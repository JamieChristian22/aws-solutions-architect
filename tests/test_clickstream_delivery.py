"""Offline contract tests for Kinesis partial retries and Firehose delivery limits.

Extract the handler so the test never creates AWS clients or contacts any service.
"""
import ast
import base64
import json
from pathlib import Path
import time
import unittest

SOURCE = (Path(__file__).resolve().parents[1]
          / "clickstream-analytics/lambda/processor/handler.py")


class RecordingFirehose:
    def __init__(self, failing=None, raise_error=False):
        self.calls = []
        self.failing = set(failing or ())
        self.raise_error = raise_error

    def put_record_batch(self, DeliveryStreamName, Records):
        self.calls.append((DeliveryStreamName, Records))
        if self.raise_error:
            raise OSError("synthetic Firehose outage")
        start = sum(len(batch) for _, batch in self.calls[:-1])
        responses = [
            {"ErrorCode": "ServiceUnavailableException"} if start + i in self.failing
            else {"RecordId": f"synthetic-{start+i}"}
            for i in range(len(Records))
        ]
        return {"RequestResponses": responses,
                "FailedPutCount": sum("ErrorCode" in item for item in responses)}


class RecordingSearch:
    def __init__(self, fail_id=None):
        self.calls = []
        self.fail_id = fail_id

    def index(self, index, id, body, refresh):
        self.calls.append((index, id, body, refresh))
        if id == self.fail_id:
            raise OSError("synthetic search outage")


def isolate_handler(firehose, search=None):
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    function = next(x for x in tree.body
                    if isinstance(x, ast.FunctionDef) and x.name == "handler")
    module = ast.Module(body=[function], type_ignores=[])
    space = {"base64": base64, "json": json, "time": time,
             "firehose": firehose, "search": search,
             "delivery_stream": "synthetic-stream", "os_index": "events",
             "MAX_FIREHOSE_RECORDS": 500,
             "MAX_FIREHOSE_BATCH_BYTES": 4 * 1024 * 1024,
             "MAX_FIREHOSE_RECORD_BYTES": 1024 * 1024}
    exec(compile(module, str(SOURCE), "exec"), space)
    return space["handler"]


def record(n, payload=None):
    payload = payload if payload is not None else {"event_id": f"event-{n}", "kind": "pageview"}
    return {"eventID": f"shard-000:{n}",
            "kinesis": {"sequenceNumber": str(n),
                        "data": base64.b64encode(json.dumps(payload).encode()).decode()}}


class DeliveryTests(unittest.TestCase):
    def test_accepts_valid_batch_and_search_indexes_same_event_id(self):
        firehose, search = RecordingFirehose(), RecordingSearch()
        result = isolate_handler(firehose, search)({"Records": [record(10), record(11)]}, None)
        self.assertEqual(result, {"batchItemFailures": []})
        self.assertEqual(len(firehose.calls), 1)
        self.assertEqual([x[1] for x in search.calls], ["event-10", "event-11"])

    def test_failing_firehose_record_uses_sequence_number_not_event_id(self):
        firehose, search = RecordingFirehose(failing={1}), RecordingSearch()
        result = isolate_handler(firehose, search)({"Records": [record(10), record(11)]}, None)
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "11"}]})
        self.assertEqual([x[1] for x in search.calls], ["event-10"])

    def test_more_than_500_records_are_split_before_firehose(self):
        firehose = RecordingFirehose()
        result = isolate_handler(firehose)({"Records": [record(i) for i in range(501)]}, None)
        self.assertEqual(result["batchItemFailures"], [])
        self.assertEqual([len(batch) for _, batch in firehose.calls], [500, 1])

    def test_batch_level_delivery_exception_returns_all_sequences(self):
        firehose = RecordingFirehose(raise_error=True)
        result = isolate_handler(firehose)({"Records": [record(1), record(2)]}, None)
        self.assertEqual(result, {"batchItemFailures": [
            {"itemIdentifier": "1"}, {"itemIdentifier": "2"}]})

    def test_invalid_json_and_missing_event_id_fail_without_delivery(self):
        firehose = RecordingFirehose()
        invalid = record(4, {"unrelated": True})
        result = isolate_handler(firehose)({"Records": [invalid, record(5)]}, None)
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "4"}]})
        self.assertEqual(len(firehose.calls[0][1]), 1)

    def test_oversize_record_does_not_enter_batch(self):
        firehose = RecordingFirehose()
        huge = record(9, {"event_id": "e9", "message": "x" * (1024*1024)})
        result = isolate_handler(firehose)({"Records": [huge]}, None)
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "9"}]})
        self.assertEqual(firehose.calls, [])

    def test_search_error_marks_delivered_record_for_retry(self):
        firehose, search = RecordingFirehose(), RecordingSearch(fail_id="event-8")
        result = isolate_handler(firehose, search)({"Records": [record(8)]}, None)
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "8"}]})
        self.assertEqual(len(firehose.calls), 1)


if __name__ == "__main__":
    unittest.main()

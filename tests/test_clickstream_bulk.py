"""Offline regression tests for the clickstream OpenSearch bulk formatter."""
import ast
import json
from pathlib import Path
import unittest
from urllib.parse import urljoin

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "clickstream-analytics/lambda/stream_processor/index.py"
)

class RecordingHttp:
    def __init__(self):
        self.requests = []

    def request(self, method, url, body, headers):
        self.requests.append((method, url, body, headers))
        return type("Response", (), {"status": 200, "data": b""})()

def isolate_bulk(endpoint="https://example.invalid/opensearch"):
    # Extract the function without importing boto3, accessing AWS, or making HTTP requests.
    source = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    function = next(node for node in source.body
                    if isinstance(node, ast.FunctionDef) and node.name == "_bulk_os")
    isolated = ast.Module(body=[function], type_ignores=[])
    http = RecordingHttp()
    values = {
        "OS_ENDPOINT": endpoint,
        "OS_SECRET_ARN": "synthetic-test-arn",
        "OS_INDEX": "events",
        "_auth_header": lambda: "Basic synthetic-test-value",
        "_http": http,
        "json": json,
        "urljoin": urljoin,
    }
    exec(compile(isolated, str(SOURCE), "exec"), values)
    return values["_bulk_os"], http

class OpenSearchBulkTests(unittest.TestCase):
    def test_two_small_records_are_valid_ndjson(self):
        bulk, http = isolate_bulk()
        result = bulk([{"event": "one"}, {"event": "two"}])
        self.assertEqual(result["chunks_ok"], 1)
        self.assertEqual(len(http.requests), 1)
        method, url, body, headers = http.requests[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/_bulk"))
        self.assertEqual(headers["Content-Type"], "application/x-ndjson")
        self.assertTrue(body.endswith(b"\n"))
        parts = [json.loads(line) for line in body.splitlines()]
        self.assertEqual(parts, [
            {"index": {"_index": "events"}}, {"event": "one"},
            {"index": {"_index": "events"}}, {"event": "two"}
        ])

    def test_large_records_never_split_across_requests(self):
        bulk, http = isolate_bulk()
        result = bulk([{"value": "a" * 1_150_000}, {"value": "b" * 1_150_000}])
        self.assertEqual(result["chunks_ok"], 2)
        self.assertEqual(len(http.requests), 2)
        for request in http.requests:
            body = request[2]
            self.assertTrue(body.endswith(b"\n"))
            lines = body.splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0]), {"index": {"_index": "events"}})
            self.assertIn("value", json.loads(lines[1]))

    def test_oversized_single_record_is_rejected(self):
        bulk, _ = isolate_bulk()
        with self.assertRaisesRegex(ValueError, "exceeds"):
            bulk([{"value": "x" * (2 * 1024 * 1024)}])

    def test_missing_endpoint_skips_without_network(self):
        bulk, http = isolate_bulk(endpoint="")
        self.assertEqual(bulk([{"event": "one"}]), {"skipped": True})
        self.assertEqual(http.requests, [])

if __name__ == "__main__":
    unittest.main()

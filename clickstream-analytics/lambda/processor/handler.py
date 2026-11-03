"""Kinesis clickstream -> Firehose and optional OpenSearch.

Partial failures use Kinesis sequence numbers, not eventID strings. Firehose is
at-least-once: use the business event_id to deduplicate downstream on retries.
"""
import base64
import json
import os
import time

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

firehose = boto3.client("firehose")
region = os.environ["AWS_REGION"]
delivery_stream = os.environ["DELIVERY_STREAM"]
os_host = os.environ.get("OS_HOST", "")
os_index = os.environ.get("OS_INDEX", "clickstream-events")
MAX_FIREHOSE_RECORDS = 500
MAX_FIREHOSE_BATCH_BYTES = 4 * 1024 * 1024
MAX_FIREHOSE_RECORD_BYTES = 1024 * 1024

search = None
if os_host:
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, "es")
    search = OpenSearch(
        hosts=[{"host": os_host, "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=10,
    )


def handler(event, context):
    """Forward valid records and return only sequence numbers requiring retry."""
    failed = set()
    pending = []
    delivered = []
    current_bytes = 0

    def flush():
        nonlocal current_bytes
        if not pending:
            return
        records = [{"Data": item[2]} for item in pending]
        try:
            reply = firehose.put_record_batch(
                DeliveryStreamName=delivery_stream, Records=records
            )
            responses = reply.get("RequestResponses", [])
            if len(responses) != len(pending):
                raise ValueError("Firehose returned an incomplete batch response")
            for (sequence, payload, _), outcome in zip(pending, responses):
                if outcome.get("ErrorCode") or not outcome.get("RecordId"):
                    failed.add(sequence)
                else:
                    delivered.append((sequence, payload))
        except Exception:
            # A batch-level exception may mean an ambiguous write. Retry with
            # downstream event_id deduplication rather than silently dropping it.
            failed.update(sequence for sequence, _, _ in pending)
        finally:
            pending.clear()
            current_bytes = 0

    for record in event.get("Records", []):
        sequence = record["kinesis"]["sequenceNumber"]
        try:
            raw = base64.b64decode(record["kinesis"]["data"], validate=True)
            payload = json.loads(raw)
            if not isinstance(payload, dict) or not isinstance(payload.get("event_id"), str) or not payload["event_id"]:
                raise ValueError("Missing event_id")
            payload["processed_at_epoch_ms"] = int(time.time() * 1000)
            data = (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")
            if len(data) > MAX_FIREHOSE_RECORD_BYTES:
                raise ValueError("Firehose record exceeds the one-MiB limit")
        except (ValueError, TypeError, KeyError, UnicodeError):
            failed.add(sequence)
            continue

        if (len(pending) >= MAX_FIREHOSE_RECORDS or
                current_bytes + len(data) > MAX_FIREHOSE_BATCH_BYTES):
            flush()
        pending.append((sequence, payload, data))
        current_bytes += len(data)

    flush()

    if search is not None:
        for sequence, payload in delivered:
            try:
                # Stable IDs make retry writes idempotent in OpenSearch.
                search.index(index=os_index, id=payload["event_id"], body=payload, refresh=False)
            except Exception:
                failed.add(sequence)

    # Lambda Kinesis partial-batch response identifies failing sequence numbers.
    return {"batchItemFailures": [{"itemIdentifier": s} for s in sorted(failed)]}

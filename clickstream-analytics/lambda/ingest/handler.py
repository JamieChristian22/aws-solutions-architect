import base64, json, os, time, uuid
import boto3
from jsonschema import Draft202012Validator, FormatChecker

kinesis = boto3.client("kinesis")
STREAM_NAME = os.environ["STREAM_NAME"]
MAX_BYTES = 64 * 1024

with open(os.path.join(os.path.dirname(__file__), "event_schema.json"), "r", encoding="utf-8") as f:
    SCHEMA = json.load(f)

validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

def response(code, body):
    return {"statusCode": code, "headers": {"content-type":"application/json"}, "body": json.dumps(body)}

def handler(event, context):
    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")

    if len(raw.encode("utf-8")) > MAX_BYTES:
        return response(413, {"error":"payload_too_large"})

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return response(400, {"error":"invalid_json"})

    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        return response(400, {"error":"schema_validation_failed","details":[e.message for e in errors[:5]]})

    envelope = {
        **payload,
        "ingested_at_epoch_ms": int(time.time() * 1000),
        "request_id": context.aws_request_id
    }
    kinesis.put_record(
        StreamName=STREAM_NAME,
        PartitionKey=payload["session_id"],
        Data=json.dumps(envelope, separators=(",",":")).encode("utf-8")
    )
    return response(202, {"accepted": True, "event_id": payload["event_id"]})

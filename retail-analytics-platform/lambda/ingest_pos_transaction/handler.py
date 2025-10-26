import json
import boto3
import os
from datetime import datetime, timezone

kinesis = boto3.client('kinesis')
STREAM_NAME = os.environ.get("STREAM_NAME", "retail-pos-stream")

def handler(event, context):
    # event expected from API Gateway: body is JSON string
    if "body" in event:
        payload = json.loads(event["body"])
    else:
        payload = event

    # basic validation
    required_fields = ["store_id", "item_id", "qty_sold", "unit_price", "timestamp_local"]
    for field in required_fields:
        if field not in payload:
            return {"statusCode":400, "body":json.dumps({"error":f"missing {field}"})}

    # normalize timestamp to UTC ISO8601
    now_utc = datetime.now(timezone.utc).isoformat()
    payload["ingested_utc"] = now_utc

    # derive gross_margin placeholder
    # NOTE: in real life you'd join product cost; here we fake it
    try:
        unit_price = float(payload["unit_price"])
        payload["gross_margin_est"] = round(unit_price * 0.32, 2)
    except:
        payload["gross_margin_est"] = None

    # push record to Kinesis
    kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(payload),
        PartitionKey=str(payload["store_id"])
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "OK", "forwarded": True})
    }

import json
import boto3
import os

kinesis = boto3.client("kinesis")

def handler(event, context):
    body = json.loads(event.get("body", "{}"))

    record = {
        "patient_id": body.get("patient_id"),
        "status": body.get("status"),
        "notes": body.get("notes"),
        "timestamp": body.get("timestamp")
    }

    kinesis.put_record(
        StreamName=os.environ["OUTREACH_STREAM"],
        Data=json.dumps(record),
        PartitionKey=record["patient_id"]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "outreach event accepted"})
    }
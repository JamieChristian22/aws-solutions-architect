import os, json, hashlib, boto3, time
from datetime import datetime, timezone

kinesis = boto3.client("kinesis")
s3 = boto3.client("s3")
STREAM_NAME = os.environ["STREAM_NAME"]
BAD_BUCKET = os.environ["BAD_BUCKET"]
ALLOW = [s.strip() for s in os.environ.get("ALLOW_ORIGINS","").split(",") if s.strip()]

def scrub_pii(e):
    c = dict(e)
    if c.get("email"):
        c["email"] = "sha256:" + hashlib.sha256(str(c["email"]).encode()).hexdigest()
    for f in ("phone","address","ip"):
        c.pop(f, None)
    return c

def origin_allowed(headers):
    o = (headers or {}).get("origin") or (headers or {}).get("Origin")
    return (not o) or (not ALLOW) or (o in ALLOW)

def put_bad(s3c, obj):
    key = f"bad/{int(time.time()*1000)}.json"
    s3c.put_object(Bucket=BAD_BUCKET, Key=key, Body=json.dumps(obj).encode())

def handler(event, context):
    try:
        if not origin_allowed(event.get("headers")):
            return {"statusCode": 403, "body": json.dumps({"error": "origin_not_allowed"})}
        body = event.get("body")
        if not body:
            return {"statusCode": 400, "body": json.dumps({"error": "missing body"})}
        payload = json.loads(body)
        records = payload if isinstance(payload, list) else [payload]
        accepted = 0
        now_iso = datetime.now(timezone.utc).isoformat()
        ua = (event.get("headers") or {}).get("user-agent","")[:256]
        origin = (event.get("headers") or {}).get("origin") or (event.get("headers") or {}).get("Origin") or "unknown"
        for ev in records:
            try:
                if not all(k in ev for k in ("event_name","user_id","created_at")):
                    raise ValueError("invalid_fields")
                cleaned = scrub_pii({**ev, "received_at": now_iso, "user_agent": ua, "origin": origin})
                kinesis.put_record(StreamName=STREAM_NAME, PartitionKey=str(cleaned["user_id"]), Data=json.dumps(cleaned).encode())
                accepted += 1
            except Exception as ex:
                put_bad(s3, {"error": str(ex), "ev": ev})
        return {"statusCode": 202, "body": json.dumps({"ok": True, "accepted": accepted, "total": len(records)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error":"internal","details":str(e)})}

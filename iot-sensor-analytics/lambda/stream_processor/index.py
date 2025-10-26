import os, json, base64, boto3, urllib3, time
from urllib.parse import urljoin
import certifi

firehose = boto3.client("firehose")
sns = boto3.client("sns")
secrets = boto3.client("secretsmanager")

FIREHOSE_NAME   = os.environ["FIREHOSE_NAME"]
SNS_TOPIC_ARN   = os.environ["SNS_TOPIC_ARN"]
OS_ENDPOINT     = os.environ.get("OS_ENDPOINT")
OS_INDEX        = os.environ.get("OS_INDEX", "iot-telemetry")
OS_SECRET_ARN   = os.environ.get("OS_SECRET_ARN")

TEMP_MAX_C      = float(os.environ.get("TEMP_MAX_C", "80"))
VIB_MAX_G       = float(os.environ.get("VIB_MAX_G", "5.0"))
BATTERY_MIN_PCT = float(os.environ.get("BATTERY_MIN_PCT", "10"))

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

def _auth_header():
    if not OS_SECRET_ARN or not OS_ENDPOINT:
        return None
    sec = secrets.get_secret_value(SecretId=OS_SECRET_ARN)
    obj = json.loads(sec["SecretString"])
    user = obj.get("username", "master-user")
    pwd  = obj.get("password", obj.get("master_user_password"))
    import base64 as b64
    token = b64.b64encode(f"{user}:{pwd}".encode()).decode()
    return "Basic " + token

def detect_anomalies(rec):
    issues = []
    if rec.get("temp_c") and rec["temp_c"] > TEMP_MAX_C:
        issues.append("TEMP_SPIKE")
    if rec.get("vibration_g") and rec["vibration_g"] > VIB_MAX_G:
        issues.append("VIBRATION_SPIKE")
    if rec.get("battery_pct") and rec["battery_pct"] < BATTERY_MIN_PCT:
        issues.append("LOW_BATTERY")
    return issues

def publish_alert(device_id, issues, record):
    if not issues:
        return
    msg = {
        "device_id": device_id,
        "issues": issues,
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sample": record,
    }
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"IoT Alert {device_id}: {','.join(issues)}",
        Message=json.dumps(msg)
    )

def bulk_index_os(docs):
    if not docs or not OS_ENDPOINT:
        return
    auth = _auth_header()
    ndjson_lines = []
    for d in docs:
        ndjson_lines.append(json.dumps({"index": {"_index": OS_INDEX}}))
        ndjson_lines.append(json.dumps(d, separators=(",", ":")))
    body = ("\n".join(ndjson_lines) + "\n").encode()
    url = urljoin(OS_ENDPOINT if OS_ENDPOINT.endswith('/') else OS_ENDPOINT+'/', "_bulk")
    r = http.request("POST", url, body=body, headers={
        "Content-Type": "application/x-ndjson",
        "Authorization": auth,
        "Connection": "keep-alive",
    })
    if r.status >= 300:
        print("OpenSearch bulk error", r.status, r.data[:300])

def handler(event, context):
    firehose_batch = []
    os_docs = []
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    for rec in event.get("Records", []):
        raw = json.loads(base64.b64decode(rec["kinesis"]["data"]).decode("utf-8"))

        enriched = {
            "device_id": raw.get("device_id"),
            "ts": raw.get("ts"),  # device timestamp
            "ingested_at": now_iso,
            "temp_c": raw.get("temp_c"),
            "humidity_pct": raw.get("humidity_pct"),
            "vibration_g": raw.get("vibration_g"),
            "battery_pct": raw.get("battery_pct"),
        }

        issues = detect_anomalies(enriched)
        enriched["anomalies"] = issues

        publish_alert(enriched["device_id"], issues, enriched)

        firehose_batch.append({"Data": (json.dumps(enriched) + "\n").encode("utf-8")})
        os_docs.append(enriched)

    if firehose_batch:
        firehose.put_record_batch(
            DeliveryStreamName=FIREHOSE_NAME,
            Records=firehose_batch
        )

    if os_docs:
        bulk_index_os(os_docs)

    return {
        "ok": True,
        "processed": len(firehose_batch),
        "alerted": sum(1 for d in os_docs if d.get("anomalies")),
    }

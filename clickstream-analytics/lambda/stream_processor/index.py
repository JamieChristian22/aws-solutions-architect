import os, json, base64, boto3, urllib3
from urllib.parse import urljoin
import certifi
import time

firehose = boto3.client("firehose")
secrets = boto3.client("secretsmanager")

FIREHOSE_NAME = os.environ.get("FIREHOSE_NAME")
OS_ENDPOINT   = os.environ.get("OS_ENDPOINT")          # https://vpc-xxxxx.region.es.amazonaws.com
OS_INDEX      = os.environ.get("OS_INDEX", "clickstream-events")
OS_SECRET_ARN = os.environ.get("OS_SECRET_ARN")

_http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

def _auth_header():
    if not OS_SECRET_ARN:
        return None
    sec = secrets.get_secret_value(SecretId=OS_SECRET_ARN)
    payload = sec.get("SecretString") or "{}"
    obj = json.loads(payload)
    user = obj.get("username", "master-user")
    pwd  = obj.get("password", obj.get("master_user_password"))
    import base64 as b64
    token = b64.b64encode(f"{user}:{pwd}".encode()).decode()
    return "Basic " + token

def _bulk_os(docs):
    if not (OS_ENDPOINT and OS_SECRET_ARN and docs):
        return {"skipped": True}
    url = urljoin(OS_ENDPOINT if OS_ENDPOINT.endswith("/") else OS_ENDPOINT + "/", "_bulk")
    max_bytes = 2 * 1024 * 1024
    auth = _auth_header()
    chunks_ok = 0
    buffer = bytearray()

    def send(chunk):
        response = _http.request(
            "POST", url, body=chunk,
            headers={
                "Content-Type": "application/x-ndjson",
                "Authorization": auth,
                "Connection": "keep-alive",
            },
        )
        if response.status >= 300:
            print(f"[OS BULK ERROR] status={response.status} body={response.data[:400]!r}")
            return False
        return True

    for document in docs:
        # Keep an action line and its source document together in one request.
        entry = (
            json.dumps({"index": {"_index": OS_INDEX}}) + "\n"
            + json.dumps(document, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        if len(entry) > max_bytes:
            raise ValueError("A single OpenSearch bulk record exceeds the 2 MiB limit")
        if buffer and len(buffer) + len(entry) > max_bytes:
            if send(bytes(buffer)):
                chunks_ok += 1
            buffer.clear()
        buffer.extend(entry)
    if buffer and send(bytes(buffer)):
        chunks_ok += 1
    return {"chunks_ok": chunks_ok}

def handler(event, context):
    fh_records, os_docs = [], []
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for rec in event.get("Records", []):
        obj = json.loads(base64.b64decode(rec["kinesis"]["data"]).decode("utf-8"))
        obj.setdefault("received_at", now_iso)
        fh_records.append({"Data": (json.dumps(obj) + "\n").encode("utf-8")})
        os_docs.append(obj)
    if fh_records:
        firehose.put_record_batch(DeliveryStreamName=FIREHOSE_NAME, Records=fh_records)
    if os_docs:
        _bulk_os(os_docs)
    return {"ok": True, "count": len(fh_records), "os_indexed": len(os_docs)}

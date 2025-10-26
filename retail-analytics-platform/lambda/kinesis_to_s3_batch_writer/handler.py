import boto3, json, gzip, os, io, time
s3 = boto3.client('s3')

BUCKET = os.environ.get("RAW_BUCKET", "retail-analytics-raw")
PREFIX = os.environ.get("RAW_PREFIX", "transactions/")

def handler(event, context):
    # event['Records'] is Kinesis batch
    batch = []
    for record in event.get("Records", []):
        data_bytes = record["kinesis"]["data"]
        data_json = json.loads(
            base64.b64decode(data_bytes).decode("utf-8")
        )
        batch.append(data_json)

    if not batch:
        return {"status":"empty"}

    # create gz payload
    ts = int(time.time())
    key = f"{PREFIX}batch_{ts}.json.gz"
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="w") as gz:
        gz.write(json.dumps(batch).encode("utf-8"))
    buf.seek(0)

    s3.put_object(Bucket=BUCKET, Key=key, Body=buf.getvalue())

    return {"status":"written","s3_key":key,"count":len(batch)}

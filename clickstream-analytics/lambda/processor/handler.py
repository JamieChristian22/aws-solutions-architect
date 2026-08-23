import base64, json, os, time
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

firehose = boto3.client("firehose")
region = os.environ["AWS_REGION"]
delivery_stream = os.environ["DELIVERY_STREAM"]
os_host = os.environ.get("OS_HOST","")
os_index = os.environ.get("OS_INDEX","clickstream-events")

credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, "es")

search = None
if os_host:
    search = OpenSearch(
        hosts=[{"host": os_host, "port":443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=10
    )

def handler(event, context):
    failures = []
    firehose_batch = []

    decoded = []
    for rec in event["Records"]:
        try:
            payload = json.loads(base64.b64decode(rec["kinesis"]["data"]))
            payload["processed_at_epoch_ms"] = int(time.time()*1000)
            decoded.append((rec["eventID"], payload))
            firehose_batch.append({"Data": (json.dumps(payload)+"\n").encode("utf-8")})
        except Exception:
            failures.append({"itemIdentifier": rec["eventID"]})

    if firehose_batch:
        result = firehose.put_record_batch(
            DeliveryStreamName=delivery_stream,
            Records=firehose_batch
        )
        if result.get("FailedPutCount",0):
            failed_indexes = {i for i,r in enumerate(result["RequestResponses"]) if "ErrorCode" in r}
            for i in failed_indexes:
                failures.append({"itemIdentifier": decoded[i][0]})

    if search:
        for event_id, payload in decoded:
            try:
                search.index(index=os_index, id=payload["event_id"], body=payload, refresh=False)
            except Exception:
                # S3 remains the durable path. Search failure is retried by failing this record.
                failures.append({"itemIdentifier": event_id})

    # de-duplicate failure identifiers
    unique = {x["itemIdentifier"]: x for x in failures}
    return {"batchItemFailures": list(unique.values())}

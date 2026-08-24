import base64,json,os,time,boto3
sns=boto3.client("sns"); firehose=boto3.client("firehose")
TOPIC=os.environ["ALERT_TOPIC_ARN"]; STREAM=os.environ["DELIVERY_STREAM"]
def detect(t):
    a=[]
    if t["temperature_c"]>=85:a.append("HIGH_TEMPERATURE")
    if t["vibration_mm_s"]>=9:a.append("HIGH_VIBRATION")
    if t["battery_pct"]<=15:a.append("LOW_BATTERY")
    if t["humidity_pct"]<10 or t["humidity_pct"]>90:a.append("HUMIDITY_OUT_OF_RANGE")
    return a
def handler(event,context):
    failures=[]; out=[]
    for r in event["Records"]:
        try:
            t=json.loads(base64.b64decode(r["kinesis"]["data"]))
            a=detect(t)
            x={**t,"anomalies":a,"processed_at_epoch_ms":int(time.time()*1000)}
            out.append({"Data":(json.dumps(x)+"\n").encode()})
            if a:
                sns.publish(TopicArn=TOPIC,Subject="IoT anomaly",Message=json.dumps({"device_id":t["device_id"],"site_id":t["site_id"],"anomalies":a}))
        except Exception:
            failures.append({"itemIdentifier":r["eventID"]})
    if out:
        result=firehose.put_record_batch(DeliveryStreamName=STREAM,Records=out)
        if result.get("FailedPutCount",0):
            return {"batchItemFailures":[{"itemIdentifier":r["eventID"]} for r in event["Records"]]}
    return {"batchItemFailures":failures}

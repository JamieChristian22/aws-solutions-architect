const { FirehoseClient, PutRecordBatchCommand } = require("@aws-sdk/client-firehose");
const fh = new FirehoseClient({});
const FIREHOSE_NAME = process.env.FIREHOSE_NAME;

exports.handler = async (event)=>{
  const batch = [];
  for(const r of (event.Records||[])){
    const data = JSON.parse(Buffer.from(r.kinesis.data, "base64").toString("utf8"));
    batch.push({ Data: Buffer.from(JSON.stringify(data)+"\n") });
  }
  if(batch.length){ await fh.send(new PutRecordBatchCommand({ DeliveryStreamName: FIREHOSE_NAME, Records: batch })); }
  return { ok:true, count: batch.length };
};

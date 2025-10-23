// services/ingest-api/index.js
const { KinesisClient, PutRecordCommand } = require('@aws-sdk/client-kinesis');

const kinesis = new KinesisClient({});
const STREAM_NAME = process.env.STREAM_NAME;

exports.handler = async (event) => {
  try {
    const body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    if (!body || !body.event || !body.ts) {
      return { statusCode: 400, body: JSON.stringify({ message: 'event and ts required' }) };
    }
    const data = Buffer.from(JSON.stringify(body));
    const partitionKey = body.user_id || 'anonymous';

    await kinesis.send(new PutRecordCommand({
      StreamName: STREAM_NAME,
      PartitionKey: partitionKey,
      Data: data
    }));

    return { statusCode: 202, body: JSON.stringify({ ok: true }) };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: JSON.stringify({ message: 'internal_error' }) };
  }
};

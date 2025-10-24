const { KinesisClient, PutRecordCommand } = require("@aws-sdk/client-kinesis");
const { S3Client, PutObjectCommand } = require("@aws-sdk/client-s3");
const crypto = require("crypto");
const kinesis = new KinesisClient({});
const s3 = new S3Client({});
const STREAM_NAME = process.env.STREAM_NAME;
const BAD_BUCKET = process.env.BAD_BUCKET;
const ALLOW = (process.env.ALLOW_ORIGINS || "").split(",").map(s => s.trim());

function scrubPII(e){ const c={...e}; if(c.email) c.email="sha256:"+crypto.createHash("sha256").update(String(c.email)).digest("hex"); delete c.phone; delete c.address; delete c.ip; return c; }
function okOrigin(h){ const o=h?.origin||h?.Origin; return !o || ALLOW.length===0 || ALLOW.includes(o); }
async function toBad(key,obj){ try{ await s3.send(new PutObjectCommand({Bucket: BAD_BUCKET, Key: `bad/${key}.json`, Body: JSON.stringify(obj)})); }catch(e){} }

exports.handler = async (event)=>{
  try{
    if(!okOrigin(event.headers)) return {statusCode:403, body: JSON.stringify({error:"origin_not_allowed"})};
    if(!event.body) return {statusCode:400, body: JSON.stringify({error:"missing body"})};
    const arr = Array.isArray(JSON.parse(event.body)) ? JSON.parse(event.body) : [JSON.parse(event.body)];
    let accepted=0;
    for(const ev of arr){
      try{
        if(!ev.event_name||!ev.user_id||!ev.created_at) throw new Error("invalid_fields");
        const cleaned = scrubPII({...ev, received_at:new Date().toISOString(), user_agent:(event.headers?.["user-agent"]||"").slice(0,256), origin:event.headers?.origin||event.headers?.Origin||"unknown"});
        await kinesis.send(new PutRecordCommand({StreamName: STREAM_NAME, PartitionKey: String(cleaned.user_id), Data: Buffer.from(JSON.stringify(cleaned))}));
        accepted++;
      }catch(ex){ await toBad(`${Date.now()}-${Math.random().toString(36).slice(2)}`, {error:String(ex), ev}); }
    }
    return {statusCode:202, body: JSON.stringify({ok:true, accepted, total:arr.length})};
  }catch(err){ return {statusCode:500, body: JSON.stringify({error:"internal", details:String(err?.message||err)})}; }
};

import argparse, concurrent.futures, json, random, time, uuid
from datetime import datetime, timezone
import requests

def event():
    return {
      "event_id":"evt-"+uuid.uuid4().hex[:20],
      "event_time":datetime.now(timezone.utc).isoformat(),
      "session_id":"sess-"+uuid.uuid4().hex[:16],
      "anonymous_id":"anon-"+uuid.uuid4().hex[:16],
      "user_id":None,
      "event_type":random.choice(["page_view","product_view","add_to_cart","checkout_start","purchase"]),
      "page_url":"/load-test",
      "referrer":None,
      "device_type":random.choice(["desktop","mobile"]),
      "source":"load_test",
      "campaign":None,
      "revenue":None,
      "properties":{"test":"capacity"}
    }

def send(url):
    t=time.perf_counter()
    try:
        r=requests.post(url,json=event(),timeout=5)
        return r.status_code,(time.perf_counter()-t)*1000
    except Exception:
        return 0,(time.perf_counter()-t)*1000

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--api-url",required=True)
    ap.add_argument("--requests",type=int,default=1000)
    ap.add_argument("--workers",type=int,default=50)
    args=ap.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        results=list(ex.map(lambda _:send(args.api_url),range(args.requests)))
    ok=sum(1 for s,_ in results if s==202)
    lat=sorted(ms for _,ms in results)
    p95=lat[int(len(lat)*0.95)-1]
    print(json.dumps({"requests":args.requests,"accepted":ok,"acceptance_rate":ok/args.requests,"p95_ms":round(p95,2)}))

if __name__=="__main__": main()

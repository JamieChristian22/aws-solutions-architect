import argparse, json, random, time, uuid
from datetime import datetime, timezone
import requests

EVENT_TYPES = ["page_view","product_view","add_to_cart","checkout_start","purchase","search","feature_use"]

def make_event():
    session = f"sess-{uuid.uuid4().hex[:16]}"
    event_type = random.choices(EVENT_TYPES, weights=[40,20,10,7,4,10,9], k=1)[0]
    revenue = round(random.uniform(15,250),2) if event_type == "purchase" else None
    return {
        "event_id": f"evt-{uuid.uuid4().hex[:20]}",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "session_id": session,
        "anonymous_id": f"anon-{uuid.uuid4().hex[:16]}",
        "user_id": None,
        "event_type": event_type,
        "page_url": "/product/SKU-44" if event_type == "product_view" else "/home",
        "referrer": None,
        "device_type": random.choice(["desktop","mobile","tablet"]),
        "source": random.choice(["organic","paid_search","email","direct","social"]),
        "campaign": None,
        "revenue": revenue,
        "properties": {"country":"US"}
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--api-url", required=True)
    p.add_argument("--events", type=int, default=100)
    p.add_argument("--rate", type=float, default=10)
    args=p.parse_args()
    interval=1/max(args.rate,0.1)
    accepted=0
    for _ in range(args.events):
        r=requests.post(args.api_url, json=make_event(), timeout=10)
        accepted += int(r.status_code == 202)
        time.sleep(interval)
    print(json.dumps({"sent":args.events,"accepted":accepted}))

if __name__=="__main__":
    main()

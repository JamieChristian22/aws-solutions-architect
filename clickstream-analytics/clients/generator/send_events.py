import json, time, uuid, random, requests, os
API = os.getenv("API_URL", "REPLACE_WITH_API_URL")
EVENTS = ["page_view","click","add_to_cart","checkout"]
URLS = ["/","/menu","/product/42","/cart"]
def gen(uid):
    return {"event_name": random.choice(EVENTS), "user_id": uid, "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "page_url": random.choice(URLS)}
if __name__ == "__main__":
    for _ in range(100):
        uid = f"u_{uuid.uuid4().hex[:8]}"
        r = requests.post(API, json=gen(uid), timeout=10)
        print(r.status_code, r.text[:120])
        time.sleep(0.05)

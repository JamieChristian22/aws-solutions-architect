import argparse,json,random,ssl,time
from datetime import datetime,timezone
import paho.mqtt.client as mqtt
def make(device,site,seq):
    temp=random.gauss(48,4); vib=max(0,random.gauss(2.5,.8)); batt=max(0,min(100,random.gauss(72,15)))
    if random.random()<.01:temp=random.uniform(85,105)
    if random.random()<.01:vib=random.uniform(9,16)
    if random.random()<.01:batt=random.uniform(3,15)
    return {"device_id":device,"site_id":site,"event_time":datetime.now(timezone.utc).isoformat(),"sequence_number":seq,
            "temperature_c":round(temp,2),"humidity_pct":round(random.uniform(25,70),2),"vibration_mm_s":round(vib,2),
            "battery_pct":round(batt,2),"firmware_version":"3.4.1","pressure_kpa":101.3,"motor_rpm":1800}
def main():
    p=argparse.ArgumentParser()
    for x in ["endpoint","device-id","site-id","cert","key","ca"]: p.add_argument("--"+x,required=True)
    p.add_argument("--count",type=int,default=60); p.add_argument("--interval",type=float,default=60)
    a=p.parse_args(); c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id=a.device_id)
    c.tls_set(a.ca,a.cert,a.key,tls_version=ssl.PROTOCOL_TLS_CLIENT); c.connect(a.endpoint,8883,60); c.loop_start()
    try:
        for i in range(a.count):
            t=make(a.device_id,a.site_id,i); topic=f"axis/{a.site_id}/{a.device_id}/telemetry"
            c.publish(topic,json.dumps(t),qos=1).wait_for_publish(); print(json.dumps(t)); time.sleep(a.interval)
    finally:c.loop_stop(); c.disconnect()
if __name__=="__main__":main()

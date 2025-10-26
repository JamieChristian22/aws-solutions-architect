import ssl, time, json, random, datetime
import paho.mqtt.client as mqtt

IOT_ENDPOINT = "REPLACE_WITH_IOT_ENDPOINT.amazonaws.com"  # AWS IoT Core endpoint
IOT_TOPIC    = "factory/line1/sensor/temperature"
CLIENT_ID    = "sensor-line1-temp-001"

# Paths to your provisioned IoT certs/keys
CA_PATH   = "./certs/AmazonRootCA1.pem"
CERT_PATH = "./certs/device.cert.pem"
KEY_PATH  = "./certs/device.private.key"

def gen_payload():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "device_id": "line1-temp-001",
        "ts": now,
        "temp_c": round(random.uniform(22.0, 90.0), 2),
        "humidity_pct": round(random.uniform(20.0, 70.0), 1),
        "vibration_g": round(random.uniform(0.1, 7.0), 2),
        "battery_pct": round(random.uniform(5.0, 100.0), 1),
    }

client = mqtt.Client(client_id=CLIENT_ID)
client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.connect(IOT_ENDPOINT, 8883)
client.loop_start()

print("Starting IoT telemetry publish loop… Ctrl+C to stop.")
try:
    while True:
        payload = gen_payload()
        client.publish(IOT_TOPIC, json.dumps(payload), qos=1)
        print("Published:", payload)
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping publisher.")
finally:
    client.loop_stop()
    client.disconnect()

import boto3, os, json

sns = boto3.client('sns')
THRESHOLD = int(os.environ.get("LOW_STOCK_THRESHOLD", "5"))
TOPIC_ARN = os.environ.get("TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:low-stock-alerts")

def handler(event, context):
    # event expected: list of {store_id, sku, on_hand_qty}
    low_items = [r for r in event.get("items", []) if r["on_hand_qty"] <= THRESHOLD]

    for item in low_items:
        message = (
            f"LOW STOCK ALERT: Store {item['store_id']} "
            f"SKU {item['sku']} on-hand {item['on_hand_qty']}"
        )
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject="Low Stock Alert"
        )

    return {
        "status":"processed",
        "alerts_sent": len(low_items)
    }

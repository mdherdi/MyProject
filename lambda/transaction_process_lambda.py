import json
import base64

def handler(event, context):
    for record in event["Records"]:
        # Decode the Kinesis data
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
       
        # Parse the JSON data
        try:
            transaction = json.loads(payload)
            print("Processing transaction:", transaction)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Raw payload: {payload}")
            continue

    return {
        "statusCode": 200,
        "body": json.dumps("Transaction processed successfully")
    }
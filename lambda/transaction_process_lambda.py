import json
import base64
import boto3
import decimal
# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("FraudulentTransactionsTable")

def extract_features(transaction):
    """Extracts basic features from the transaction for fraud detection. Adding default to prevent error by missing value"""
    
    features = {
        "high_value": 1 if transaction.get("amount",0) > 1000 else 0,
        "is_vpn": 1 if transaction.get("is_vpn", False) else 0,
        "card_type_credit": 1 if transaction.get("card_type") == "credit" else 0,
        "location_risk": 1 if transaction.get("location") in ["B", "G"] else 0
    }
    return features

def handler(event, context):
    for record in event["Records"]:

        try:
            # Decode Kinesis event data (Base64 decoding)
            raw_payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
            transaction = json.loads(raw_payload)

            print(f"Received transaction: {transaction}")

            # Extract features
            features = extract_features(transaction)
            print(f"Extracted features: {features}")

            # Fraud detection logic
            fraud_score = decimal.Decimal("0.9") if features["high_value"] or features["location_risk"] else decimal.Decimal("0.2")
            status = "fraudulent" if fraud_score > 0.8 else "not_fraudulent"


           # Store transaction in DynamoDB
            table.put_item(
                Item={
                    "transaction_id": transaction["transaction_id"],
                    "user_id": transaction.get("user_id", "unknown"),
                    "amount": transaction.get("amount", 0),
                    "fraud_score": fraud_score,
                    "status": status,
                    "features": features  # Pass as a dictionary (Map)
                }
            )
            print(f"Stored transaction in DynamoDB: {status}")
        except Exception as e:
            print(f"Error processing transaction: {e}. Record: {record}")

    return {
        "statusCode": 200,
        "body": json.dumps("Processed transactions with feature engineering.")
    }
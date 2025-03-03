import boto3
import json
import random
import uuid
import time

# Initialize the Kinesis client
kinesis_client = boto3.client("kinesis", region_name="ca-central-1")

# Name of the Kinesis stream
stream_name = "TransactionStream"

# Function to generate mock transaction data
def generate_transaction():
    return {
        "transaction_id": f"T{str(uuid.uuid4())}",
        "user_id": f"U{random.randint(10000, 99999)}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "amount": random.randint(10, 1000),
        "device_type": random.choice(["mobile", "desktop"]),
        "location": random.choice(["A", "B", "C", "D", "E", "F", "G", "H"]),
        "is_vpn": random.choice([True, False]),
        "card_type": random.choice(["credit", "debit"]),
        "status": random.choice(["approved", "declined"])
    }

# Function to send data to the Kinesis stream
def send_to_kinesis(stream_name, data):
    try:
        response = kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey=data["transaction_id"]  
        )
        print(f"Sent transaction {data['transaction_id']} to Kinesis. SequenceNumber: {response['SequenceNumber']}")
    except Exception as e:
        print(f"Error sending data to Kinesis: {e}")

# Main function to test the Kinesis stream
def main():
    print("Starting Kinesis data stream test...")
    for i in range(10):  
        transaction = generate_transaction()
        send_to_kinesis(stream_name, transaction)
        time.sleep(1)  
    print("Test completed.")

if __name__ == "__main__":
    main()
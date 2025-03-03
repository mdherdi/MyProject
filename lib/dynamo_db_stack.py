from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
import aws_cdk as cdk
from constructs import Construct

class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a DynamoDB table for processed transactions
        self.fraud_table = dynamodb.Table(
            self, 
            "FraudulentTransactionsTable",
            table_name="FraudulentTransactionsTable",
            partition_key=dynamodb.Attribute(name="transaction_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Output Table Name
        cdk.CfnOutput(self, "DynamoDBTableName", value=self.fraud_table.table_name)



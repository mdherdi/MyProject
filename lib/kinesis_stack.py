from aws_cdk import (
    Stack,
    aws_kinesis as kinesis,
)
import aws_cdk as cdk
from constructs import Construct

class KinesisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Kinesis Stream to ingest transactions
        self.kinesis_stream = kinesis.Stream(
            self,
            "TransactionStream",
            stream_name="TransactionStream",
            shard_count=1,
            retention_period=cdk.Duration.hours(24)

        )
        
        # Output Stream 
        cdk.CfnOutput(self, "kinesis_stream", value=self.kinesis_stream.stream_name)

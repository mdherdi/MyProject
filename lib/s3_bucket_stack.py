from aws_cdk import (
    Stack,
    aws_s3 as s3,
)
import aws_cdk as cdk
from constructs import Construct

class S3BucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Bucket Resource
        self.s3_bucket = s3.Bucket(
            self, "FraudDetectionStorage",
            bucket_name="fraud-detection-storage-mk", 
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,  
            removal_policy=cdk.RemovalPolicy.RETAIN 
        )

        # Output S3 Bucket Name 
        cdk.CfnOutput(self, "S3BucketName", value=self.s3_bucket.bucket_name)



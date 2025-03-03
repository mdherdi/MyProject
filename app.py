#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lib.s3_bucket_stack import S3BucketStack
from lib.kinesis_stack import KinesisStack
from lib.lambda_stack import LambdaStack
from lib.dynamo_db_stack import DynamoDBStack

app = cdk.App()

kinesis_stack = KinesisStack(app,"KinesisDemoStack")
dynamodb_stack = DynamoDBStack(app, "DynamoDBDemoStack")
s3_stack = S3BucketStack(app, "S3DemoBucket")
lambda_stack = LambdaStack(app, "LambdaDemoStack", kinesis_stream=kinesis_stack.kinesis_stream,dynamodb_table=dynamodb_stack.fraud_table, s3_bucket=s3_stack.s3_bucket)



app.synth()
    

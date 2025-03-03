#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lib.s3_bucket_stack import S3BucketStack
from lib.kinesis_stack import KinesisStack
from lib.lambda_stack import LambdaStack

app = cdk.App()
# s3_stack = S3BucketStack(app, "S3DemoBucket")
kinesis_stack = KinesisStack(app,"KinesisDemoStack")
lambda_stack = LambdaStack(app, "LambdaDemoStack", kinesis_stack.kinesis_stream)


app.synth()
    

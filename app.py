#!/usr/bin/env python3
import os

import aws_cdk as cdk

from my_project.s3_bucket_stack import S3BucketStack


app = cdk.App()
S3BucketStack(app, "TestS3Bucket")

app.synth()

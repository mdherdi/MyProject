from aws_cdk import (
    Stack,
    aws_lambda as _lambda, 
    aws_lambda_event_sources as event_sources,
    aws_iam as iam, 
    aws_dynamodb as dynamodb,
    Duration)
import aws_cdk as cdk
from constructs import Construct

class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, kinesis_stream,dynamodb_table,s3_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Lambda Function
        process_lambda = _lambda.Function(
            self,
            "ProcessLambda",
            function_name="ProcessLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,

            handler="transaction_process_lambda.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "DYNAMODB_TABLE_NAME": dynamodb_table.table_name,
                "S3_BUCKET_NAME": s3_bucket.bucket_name  
            }
        )

         # IAM Role for Lambda
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
            ]
        )
        
        dynamodb_table.grant_read_write_data(lambda_role)
        s3_bucket.grant_read_write(lambda_role)

    

         # Add an event source mapping to trigger the Lambda function from the Kinesis stream
        process_lambda.add_event_source(
            event_sources.KinesisEventSource(
            kinesis_stream,
            starting_position=_lambda.StartingPosition.LATEST
        ))

         # Output Lambda ARN
        cdk.CfnOutput(self, "LambdaARN", value=process_lambda.function_arn)

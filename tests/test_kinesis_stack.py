from aws_cdk import (
    App,
    Stack
    )
from lib.kinesis_stack import KinesisStack
import aws_cdk.assertions as assertions

def test_kinesis_stack():
    app = App()
    stack = Stack(app, "TestStack")
    kinesis_stack = KinesisStack(stack, "KinesisStack")

    template = assertions.Template.from_stack(kinesis_stack)
    template.has_resource_properties("AWS::Kinesis::Stream", {
        "ShardCount": 1
    })
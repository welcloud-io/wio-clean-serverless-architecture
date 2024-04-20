from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_lambda_event_sources as event_sources,
)
from constructs import Construct

class WioCleanServerlessArchitectureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        simple_lambda = _lambda.Function(self, "SimpleLambda",
            function_name="CleanServerlessFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="simple_lambda.handler",
            code=_lambda.Code.from_asset("lambda"),
        )
        
        api = apigw.LambdaRestApi(self, "Endpoint",
            handler=simple_lambda,
        )

        table = dynamodb.Table(self, "SimpleTable", table_name = 'CleanServerlessTable',
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )
        table.grant_read_write_data(simple_lambda)
        
        topic = sns.Topic(self, "CleanServerlessTopic",
            topic_name="CleanServerlessTopic"
        )
        topic.grant_publish(simple_lambda)
        
        sub_sms = sns.Subscription(self, "SubscriptionSMS",
            endpoint="+33600000000", # ========================> Replace with a valid phone number
            protocol=sns.SubscriptionProtocol.SMS,
            topic=topic
        )
        
        queue = sqs.Queue(self, "Queue",
            queue_name = "CleanServerlessQueue",
        )
        queue.grant_consume_messages(simple_lambda)

        simple_lambda.add_event_source(
            event_sources.SqsEventSource(queue,
                batch_size=1
            )
        )
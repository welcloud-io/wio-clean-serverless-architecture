# Building Evolutionary Serverless Architecture with AWS Lambda and the CDK

Blog post reference: https://dev.to/welcloud-io/building-evolutionary-serverless-architecture-with-aws-lambda-and-the-cdk-40e0

## Prerequisite

- Python 3.9 installed

- CDK >= 2.133 installed

## Deploy architecture

If you want to receive sms from sns:

Open 
`wio_clean_serverless_architecture/wio_clean_serverless_architecture_stack.py`

then, put a valid phone number in the sns subscription
```
        sub_sms = sns.Subscription(self, "SubscriptionSMS",
            endpoint="+33600000000", # <========== Replace with a valid phone number
            protocol=sns.SubscriptionProtocol.SMS,
            topic=topic
        )
```

In the terminal:

```
$> cdk deploy
```

## Test API

In the AWS console, go to API Gateway>Endpoint>Any>Test

Request body:
```
{
    "stock_id": "A000",
    "stock_level": 1
}
```

Click on [TEST] button

In the AWS console, Go to DynamoDB>Tables>CleanServerlessTable>Explore Table Items

Verify the item has been inserted

## Test SQS Queue

Open 
`lambda/simple_lambda.py`

replace 
`api_gateway_adapter(event)`
with
`sqs_adapter_receive_message(event)`

In the terminal:
```
$> cdk deploy
```

Execute sqs script
```
$>python put-stock-to-sqs.py
```

In the AWS console, go to DynamoDB>Tables>CleanServerlessTable>Explore Table Items

Verify the items have been inserted

---
N.B.: If configured properly, in each test you should receive a sms with a "Stock level is low" message on your cell phone
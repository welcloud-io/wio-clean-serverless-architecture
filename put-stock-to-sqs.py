import boto3

sqs = boto3.client('sqs')
sts = boto3.client('sts')

def current_aws_account_number():
    return sts.get_caller_identity().get('Account')

with open('./put-stock.txt', 'r') as f:
    for line in f:
        line = line.strip()
        response = sqs.send_message(
            QueueUrl = f'https://sqs.eu-west-1.amazonaws.com/{current_aws_account_number()}/CleanServerlessQueue',
            MessageBody = (line)
        )
        
        print(response)
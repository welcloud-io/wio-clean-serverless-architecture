import boto3, json
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

account_id = boto3.client('sts').get_caller_identity().get('Account')

# ------------------------------------------------------------------------------
# INPUT Adapters
# ------------------------------------------------------------------------------
def api_gateway_adapter(event):
    body = json.loads(event.get('body'))
    stock_id = body['stock_id']
    stock_level = int(body['stock_level'])
    stock_update_input_request(stock_id, stock_level)

def sqs_adapter_receive_message(event):
    message = event.get('Records')[0].get('body')
    stock_id = message.split(';')[0]
    stock_level = int(message.split(';')[1])
    stock_update_input_request(stock_id, stock_level)

# ------------------------------------------------------------------------------
# INPUT Ports
# ------------------------------------------------------------------------------ 
def stock_update_input_request(stock_id, stock_level):
    stock_update(stock_id, stock_level)

# ------------------------------------------------------------------------------
# DOMAIN
# ------------------------------------------------------------------------------
def stock_update(stock_id, stock_level):
    update_stock_level(stock_id, stock_level)

    if stock_level <= 1:
        send_notification('Stock level is low')

# ------------------------------------------------------------------------------
# OUTPUT Ports
# ------------------------------------------------------------------------------        
def update_stock_level(stock_id, stock_level):
    dynamodb_adapter_update_stock_level(stock_id, stock_level)
    
def send_notification(message):
    sns_adapter_send_notification(message)

# ------------------------------------------------------------------------------
# OUTPUT Adapters
# ------------------------------------------------------------------------------
def dynamodb_adapter_update_stock_level(stock_id, stock_level):
    table = dynamodb.Table('CleanServerlessTable')
    table.update_item(
        Key={
            'id': stock_id
        },
        UpdateExpression='SET stock_level = :val1',
        ExpressionAttributeValues={
            ':val1': stock_level
        }
    )
    
def sns_adapter_send_notification(message):
    sns.publish(
        TopicArn=f'arn:aws:sns:eu-west-1:{account_id}:CleanServerlessTopic',
        Message=message
    )
    
# ------------------------------------------------------------------------------
# LAMBDA HANDLER
# ------------------------------------------------------------------------------
def handler(event, context):
    api_gateway_adapter(event)

    return {
        'statusCode': 200,
        'body': 'Success'
    }
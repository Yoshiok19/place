import json
import redis
import boto3
import base64

# Using: https://redis.io/docs/latest/develop/clients/redis-py/
# Using:  https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-to-your-production-redis-with-tls
# Had to be on the same VPC (Simplest to create the lambda on the VPC, but you can figure this out)
# Had to use ssl=True
sqs_client = boto3.client('sqs', region_name='us-east-2') 
queue_url = 'https://sqs.us-east-2.amazonaws.com/905418190027/place2InitializeQueue'
r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)
gateway = boto3.client('apigatewaymanagementapi', endpoint_url="https://8pcetrce1k.execute-api.us-east-2.amazonaws.com/production")

def lambda_handler(event, context):
    print(event)
    connectionId = event["requestContext"]["connectionId"];

    # Example: Sending a message
    try:
        send_response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=f'{connectionId}'
        )
        print(f"Message sent! ID: {send_response['MessageId']}")
    except Exception as e:
        print(f"Error sending message: {e}")

    res = r.sadd('clients', connectionId)
    clients = r.smembers('clients')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


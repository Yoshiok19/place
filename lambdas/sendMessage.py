import json
import redis
import boto3

# Using: https://redis.io/docs/latest/develop/clients/redis-py/
# Using:  https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-to-your-production-redis-with-tls
# Had to be on the same VPC (Simplest to create the lambda on the VPC, but you can figure this out)
# Had to use ssl=True

r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)
gateway = boto3.client('apigatewaymanagementapi', endpoint_url="https://8pcetrce1k.execute-api.us-east-2.amazonaws.com/production/")
sqs_client = boto3.client('sqs', region_name='us-east-2') 

queue_url = 'https://sqs.us-east-2.amazonaws.com/905418190027/requestQueue'

def lambda_handler(event, context):
    print(event)
    connectionId = event["requestContext"]["connectionId"]
    message = json.loads(event["body"])
    pixels = message['data']

    history_data = []
    canvas_data = {}
    for pixel in pixels:
        history_data.append(json.dumps(pixel))
        key = str(pixel['x']) + " " + str(pixel['y'])
        rgb = {
            'r': pixel['r'],
            'g': pixel['g'],
            'b': pixel['b']
        }
        canvas_data[key] = json.dumps(rgb)

    # Append changes to history
    r.rpush("history", *history_data)
    # Update canvas in redis
    r.hmset("canvas", canvas_data)

    try:
        send_response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(
                history_data
            )
        )
        print(f"Message sent! ID: {send_response['MessageId']}")
    except Exception as e:
        print(f"Error sending message: {e}")

    return { "statusCode": 200  }


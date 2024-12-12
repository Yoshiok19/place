import json
import boto3
import redis 

url = f"https://8pcetrce1k.execute-api.us-east-2.amazonaws.com/production"
gateway = boto3.client('apigatewaymanagementapi', endpoint_url=url)
r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)

def lambda_handler(event, context):
    print(event)

    for record in event["Records"]:
        try:
            canvas = r.hgetall('canvas')
            connectionId = record['body']
            print("CANVAS", canvas, type(canvas))
            payload = {
                'type': 'init',
                'data': canvas
            }
            response = gateway.post_to_connection(ConnectionId=connectionId, Data=json.dumps(payload).encode('utf-8'))
        except:
            continue
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

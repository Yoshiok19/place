import json
import redis
import boto3

# Using: https://redis.io/docs/latest/develop/clients/redis-py/
# Using:  https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-to-your-production-redis-with-tls
# Had to be on the same VPC (Simplest to create the lambda on the VPC, but you can figure this out)
# Had to use ssl=True

r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)
url = f"https://8pcetrce1k.execute-api.us-east-2.amazonaws.com/production"
gateway = boto3.client('apigatewaymanagementapi', endpoint_url=url)

def lambda_handler(event, context):
    
    clients = r.smembers('clients')
    for record in event["Records"]:
        pixels = record["body"]
        payload = {
            'type': 'update',
            'data': pixels
        }
        for client in clients:
            try:
                response = gateway.post_to_connection(ConnectionId=client, Data=json.dumps(payload).encode('utf-8'))
            except:
                r.srem('clients', client)
            
    
    return {
        'statusCode': 200
    }


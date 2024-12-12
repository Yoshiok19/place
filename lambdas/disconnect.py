import json
import redis 

# Using: https://redis.io/docs/latest/develop/clients/redis-py/
# Using:  https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-to-your-production-redis-with-tls
# Had to be on the same VPC (Simplest to create the lambda on the VPC, but you can figure this out)
# Had to use ssl=True

r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)

def lambda_handler(event, context):
    connectionId = event["requestContext"]["connectionId"]
    r.srem('clients', connectionId)
    clients = r.smembers('clients')
    print(clients)
    return {
        'statusCode': 200
    }


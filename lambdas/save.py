import json
import redis
import boto3
from datetime import datetime, timezone, timedelta

from dyno_tables.mru_pixels import MruPixels
from dyno_tables.pixel_history import PixelHistory

# Using: https://redis.io/docs/latest/develop/clients/redis-py/
# Using:  https://redis.io/docs/latest/develop/clients/redis-py/connect/#connect-to-your-production-redis-with-tls
# Had to be on the same VPC (Simplest to create the lambda on the VPC, but you can figure this out)
# Had to use ssl=True

r = redis.Redis(host='placev2cache-k5khko.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)
gateway = boto3.client('apigatewaymanagementapi', endpoint_url="https://8pcetrce1k.execute-api.us-east-2.amazonaws.com/production/")
dynamodb = boto3.resource('dynamodb')

mru_pixels_table = MruPixels(dyn_resource=dynamodb)
pixel_history_table = PixelHistory(dyn_resource=dynamodb)

mru_pixels_table.exists('mru_pixels')
pixel_history_table.exists('pixel_history')

def lambda_handler(event, context):
    print(event)

    # Append change to history (For scribble_v2)
    # r.rpush("history", json.dumps(pixel))
    # history = r.lrange("history", 0, -1)
    
    # Update canvas in redis

    lst = []

    hist_len = r.llen('history')
    time_change = timedelta(minutes=100)
    one_sec = timedelta(seconds=1)
    timestamp = datetime.now(timezone.utc) - time_change
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    for _ in range(hist_len):
        pixel = json.loads(r.lpop('history'))
        pos = str(pixel['x']) + " " + str(pixel['y'])
        rgb = str(pixel['r']) + " " + str(pixel['g']) + " " + str(pixel['b'])
        lst.append({ 'pixel': pos, 't': timestamp_str, 'rgb':rgb })
        timestamp += one_sec
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    pixel_history_table.add_pixels(lst)

    lst.clear()

    redis_canvas = r.hgetall("canvas")

    for pos in redis_canvas:
        rgb = json.loads(redis_canvas[pos])
        rgb = str(rgb['r']) + " " + str(rgb['g']) + " " + str(rgb['b'])
        lst.append({ 'pixel': pos, 't': timestamp_str, 'rgb':rgb })
        timestamp += one_sec
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    mru_pixels_table.update_pixels(lst)

    return { "statusCode": 200  }


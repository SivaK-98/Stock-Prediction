import redis

def push_to_redis(data):
    redis_cli = redis.Redis(
  host='redis-12484.c212.ap-south-1-1.ec2.redns.redis-cloud.com',
  port=12484,
  password='RscHf9E2waXKeNws98yTQU8grVDUiGgR')
    symbol = data["symbol"]
    last_price = data["lastprice"]
    result = redis_cli.set(symbol,last_price)
    print("Redis result:",result)
    return "success"
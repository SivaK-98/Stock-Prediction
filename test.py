import redis
import requests
import os
# Redis connection settings
REDIS_HOST = os.getenv("redis_host")
REDIS_PORT = 12484
REDIS_DB = 0
redis_password = os.getenv("redis_password")

# Grafana connection settings
GRAFANA_HOST = 'https://awstestuser1998.grafana.net/'
GRAFANA_API_KEY = os.getenv("grafana_token")
GRAFANA_DATASOURCE_NAME = 'live_stock_data'

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           password=redis_password)
# Get data from Redis
#
for key in redis_client.keys():
    value = redis_client.get(key).decode('utf-8')
    print(f"Key: {key.decode('utf-8')}, Value: {value}")
"""


# Convert data to a format that Grafana can understand
metrics = []
for key, value in data.items():
    metric = {
        'etric': key,
        'value': value,
        'timestamp': int(redis_client.hget('my_data', 'timestamp'))
    }
    metrics.append(metric)

# Send data to Grafana using the Grafana API
headers = {
    'Authorization': f'Bearer {GRAFANA_API_KEY}',
    'Content-Type': 'application/json'
}
response = requests.post(
    f'{GRAFANA_HOST}/api/datasources/proxy/{GRAFANA_DATASOURCE_NAME}/write',
    headers=headers,
    json={'metrics': metrics})

if response.status_code == 204:
    print('Data sent to Grafana successfully!')
else:
    print('Error sending data to Grafana:', response.text)
"""

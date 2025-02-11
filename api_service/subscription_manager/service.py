import requests
import os
from pymemcache.client import base

MEMCACHED_HOST = os.getenv('MEMCACHED_HOST', 'localhost')
MEMCACHED_PORT = int(os.getenv('MEMCACHED_PORT', 11211))
MEMCACHED_SUB_PREFIX = 'sub_'

def getCacheClient():
    return base.Client((MEMCACHED_HOST, MEMCACHED_PORT))

class Validation():
    def __init__(self, isValid:bool, subscription:str):
        self.isValid = isValid
        self.subscription = subscription

def isValidToken(apiKey: str):
    cacheClient = getCacheClient()
    cacheValue = cacheClient.get(MEMCACHED_SUB_PREFIX + apiKey)
    if (cacheValue):
        return Validation(True, cacheValue.decode('utf-8'))
    else:
        response = requests.get('http://subscription_manager:5004/auth?api_key=' + apiKey)
        if response.status_code == 200:
            json = response.json()
            cacheClient.set(MEMCACHED_SUB_PREFIX + apiKey, json['subscription'])
            return Validation(True, json['subscription'])
        else:
            return Validation(False, None)
        
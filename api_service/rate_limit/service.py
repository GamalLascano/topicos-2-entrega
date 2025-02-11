import os
from pymemcache.client import base

MEMCACHED_HOST = os.getenv('MEMCACHED_HOST', 'localhost')
MEMCACHED_PORT = int(os.getenv('MEMCACHED_PORT', 11211))
MEMCACHED_RATE_PREFIX = 'rate_'
FREEMIUM_SUBSCRIPTION_RATE = 5
PREMIUM_SUBSCRIPTION_RATE = 50

SUBSCRIPTION_RATES = {'freemium': FREEMIUM_SUBSCRIPTION_RATE, 'premium': PREMIUM_SUBSCRIPTION_RATE}

def getCacheClient():
    return base.Client((MEMCACHED_HOST, MEMCACHED_PORT))

def isRateLimited(apiKey: str, subscription: str):
    cacheClient = getCacheClient()
    cacheValue = cacheClient.get(MEMCACHED_RATE_PREFIX + apiKey)
    if (cacheValue):
        rate = int(cacheValue.decode('utf-8'))
        limit = SUBSCRIPTION_RATES.get(subscription)
        if limit is None:
            return False
        if (rate >= limit):
            return True
        cacheClient.incr(MEMCACHED_RATE_PREFIX + apiKey, 1)
        return False
    cacheClient.set(MEMCACHED_RATE_PREFIX + apiKey, 1, 60)
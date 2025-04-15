# -*- coding: utf-8 -*-

# Caching
# https://docs.djangoproject.com/en/2.2/topics/cache/
from config.settings.components import env


REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env("REDIS_PORT", default=6379)

RQ_QUEUES = {
    "default": {
        "URL": f"redis://{REDIS_HOST}:{REDIS_PORT}/queues",
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/cache",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

# -*- coding: utf-8 -*-
from config.settings.components import env

REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_PORT = env("REDIS_PORT", default=6379)

CONSTANCE_CONFIG = {
    'OTP_VALIDATION_URL': ('', 'It helps to format OTP SMSs', str),
    'APP_RELEASE_VERSION_NAME': ('0.50.0', 'Version name of the app', str),
    'APP_RELEASE_VERSION_CODE': (50, 'Version code of the app', int),
    'APP_RELEASE_MANDATORY': (False, 'Is the app upgrade mandatory?', bool),
}
CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_REDIS_CONNECTION = env(f'redis://{REDIS_HOST}:{REDIS_PORT}/constance', default='redis://redis:6379/0')

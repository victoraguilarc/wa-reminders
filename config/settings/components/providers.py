# -*- encoding: utf-8 -*-

from config.settings.components import env

ALLOWED_TENANTS_LIMIT = env.int('ALLOWED_TENANTS_LIMIT', default=5)

PUSHER_APP_ID = env('PUSHER_APP_ID')
PUSHER_KEY = env('PUSHER_KEY')
PUSHER_SECRET = env('PUSHER_SECRET')
PUSHER_HOST = env('PUSHER_HOST')

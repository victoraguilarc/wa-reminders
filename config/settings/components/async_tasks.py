# -*- coding: utf-8 -*-
#
# A S Y N C  T A S K S
#
from config.settings.components import env

ASYNC_TASKS_QUEUE_URL = env('ASYNC_TASKS_QUEUE_URL')

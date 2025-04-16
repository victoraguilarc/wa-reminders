# -*- coding: utf-8 -*-
import os

from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = 'src.common'
    verbose_name = 'Common'

    def ready(self):
        # if 'runserver' not in sys.argv:
        #     return

        if os.environ.get('RUN_MAIN') != 'true':
            return

        # from src.notifications.infrastructure.scheduled_tasks import register_jobs
        # register_jobs()

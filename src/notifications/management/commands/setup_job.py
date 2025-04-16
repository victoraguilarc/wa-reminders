# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.infrastructure.tasks.health import check_scheduler


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()

        app_context.scheduler.add_job(
            check_scheduler,
            trigger='interval',
            seconds=10,
        )

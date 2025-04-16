# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from loguru import logger

from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()

        app_context.scheduler.start()
        logger.info(">>> Scheduler started...")


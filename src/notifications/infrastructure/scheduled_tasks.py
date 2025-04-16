# -*- coding: utf-8 -*-

from loguru import logger

from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.infrastructure.tasks.health import check_scheduler


def register_jobs():
    app_context = AppContextBuilder.from_env()
    scheduler = app_context.scheduler

    scheduler.add_job(
        check_scheduler,
        trigger='interval',
        seconds=15,
    )
    logger.info(">>> Registered scheduled tasks...")

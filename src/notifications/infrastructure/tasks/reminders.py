from typing import Optional
from uuid import UUID

from apscheduler.jobstores.base import JobLookupError
from loguru import logger

from src.common.domain.entities.reminder import Reminder
from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.application.reminders.use_cases.performer import ReminderPerformer


def perform_reminder(reminder_id: str | UUID):
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    ReminderPerformer(
        reminder_id=reminder_id,
        repository=domain_context.reminder_repository,
        whatsapp_sender=domain_context.whatsapp_sender,
        whatsapp_session='default',
    ).execute()


def create_reminder_job(reminder: Reminder) -> str:
    app_context = AppContextBuilder.from_env()
    scheduler = app_context.scheduler

    scheduled_job = scheduler.add_job(
        func=perform_reminder,
        trigger='date',
        run_date=reminder.scheduled_time,
        args=[reminder.id],
    )
    logger.info(f">>> Created reminder job: {scheduled_job.id}")

    return scheduled_job.id


def update_reminder_job(reminder: Reminder) -> Optional[str]:
    app_context = AppContextBuilder.from_env()
    scheduler = app_context.scheduler

    if not reminder.scheduled_job_id:
        return None

    try:
        scheduler.modify_job(
            reminder.scheduled_job_id,
            trigger='date',
            run_date=reminder.scheduled_time,
            args=[reminder.id],
        )
        logger.info(f">>> Updated reminder job: {reminder.scheduled_job_id}")
        return reminder.scheduled_job_id

    except JobLookupError as e:
        logger.warning(f">>> Failed to update reminder job: {reminder.scheduled_job_id}, Error: {e}")
        return None


def cancel_reminder_job(reminder: Reminder) :
    app_context = AppContextBuilder.from_env()
    scheduler = app_context.scheduler

    if not reminder.scheduled_job_id:
        return None

    try:
        logger.info(f">>> Canceling reminder job: {reminder.scheduled_job_id}")
        scheduler.remove_job(reminder.scheduled_job_id)
    except JobLookupError as e:
        logger.warning(f">>> Failed to update reminder job: {reminder.scheduled_job_id}, Error: {e}")
        return None




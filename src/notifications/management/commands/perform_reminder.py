# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from src.common.domain.value_objects import ReminderId
from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.application.reminders.use_cases.performer import ReminderPerformer


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()

        ReminderPerformer(
            reminder_id=ReminderId('95bbd833-de7f-4bcf-a966-fdf281d03eab'),
            repository=app_context.domain.reminder_repository,
            whatsapp_sender=app_context.domain.whatsapp_sender,
            whatsapp_session='default',
        ).execute()


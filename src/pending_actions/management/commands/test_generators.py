# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from src.pending_actions.application.use_cases.update_publisher import (
    PendingActionSSEventPublisher,
)
from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()
        domain_context = app_context.domain

        pending_action = domain_context.pending_action_repository.find_by_tracking_code(
            tracking_code='71217c56ce944313a7f5afac330b506b',
        )

        PendingActionSSEventPublisher(
            pending_action=pending_action,
            stream_events_publisher=domain_context.stream_events_publisher,
        ).execute()

        print(f'Status Published! ')

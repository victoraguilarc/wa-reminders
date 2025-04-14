# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from src.common.database.admin.user import send_email_verification
from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()
        domain_context, bus_context = app_context.domain, app_context.bus

        send_email_verification(
            command_bus=bus_context.command_bus,
            send_to='vicobits@gmail.com',
            action_link='https://xiberty.com',
        )
        print(f'Email Sent')

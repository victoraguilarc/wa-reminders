# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from src.common.application.shortcuts.verifications import send_whatsapp_verification
from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()
        domain_context, bus_context = app_context.domain, app_context.bus

        send_whatsapp_verification(
            command_bus=bus_context.command_bus,
            phone_number='5215544586680',
            action_link='https://collectives.pro',
        )
        print(f'Whatsapp Sent')

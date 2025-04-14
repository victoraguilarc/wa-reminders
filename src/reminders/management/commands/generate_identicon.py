# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from src.common.application.queries.resources import GenerateIdenticonQuery
from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()
        domain_context, bus_context = app_context.domain, app_context.bus

        bus_context.query_bus.ask(
            query=GenerateIdenticonQuery(label='test')
        )
        print(f'Identicon Generated! ')

# -*- coding: utf-8 -*-

from django.apps import AppConfig


class TenantsConfig(AppConfig):
    """Configuration for users and permissions functionalties."""

    name = 'src.tenants'
    verbose_name = 'Tenant'
    verbose_name_plural = 'Tenants'

    def ready(self):
        from src.tenants.infrastructure.bus_wiring import wire_handlers

        wire_handlers()

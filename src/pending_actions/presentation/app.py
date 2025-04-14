# -*- coding: utf-8 -*-

from django.apps import AppConfig


class PendingActionsConfig(AppConfig):
    name = 'src.pending_actions'
    label = 'pending_actions'
    verbose_name = 'Pending Action'
    verbose_name_plural = 'Pending Actionss'

    def ready(self):
        from src.pending_actions.infrastructure.bus_wiring import wire_handlers
        wire_handlers()

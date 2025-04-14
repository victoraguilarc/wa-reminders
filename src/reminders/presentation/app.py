# -*- coding: utf-8 -*-

from django.apps import AppConfig


class RemindersConfig(AppConfig):
    name = 'src.reminders'
    verbose_name = 'Reminder'
    verbose_name_plural = 'Reminders'

    def ready(self):
        from src.reminders.infrastructure.bus_wiring import wire_handlers

        wire_handlers()

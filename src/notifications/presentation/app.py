# -*- coding: utf-8 -*-

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configuration for users and permissions functionalties."""

    name = 'src.notifications'
    verbose_name = 'Notification'
    verbose_name_plural = 'Notifications'

    def ready(self):
        from src.notifications.infrastructure.bus_wiring import wire_handlers

        wire_handlers()

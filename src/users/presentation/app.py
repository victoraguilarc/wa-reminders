# -*- coding: utf-8 -*-

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for users and permissions functionalties."""

    name = 'src.users'
    verbose_name = 'User'
    verbose_name_plural = 'Userss'

    def ready(self):
        from src.users.infrastructure.bus_wiring import wire_handlers

        wire_handlers()

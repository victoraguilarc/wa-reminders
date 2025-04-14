# -*- coding: utf-8 -*-

from typing import Optional

from django.conf import settings

from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.infrastructure.callback_builder import DjangoCallbackBuilder, PathCallbackBuilder


def get_composed_callback_builder(
    callback_hostname: Optional[str] = None,
    view_name: Optional[str] = None,
) -> CallbackBuilder:
    if callback_hostname and not view_name:
        return PathCallbackBuilder(hostname=callback_hostname)
    if view_name:
        return DjangoCallbackBuilder(settings.API_HOSTNAME, view_name)
    return PathCallbackBuilder('/')

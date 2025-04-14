# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def load_static_path(static_file: str):
    static_path = static(static_file)
    if not settings.DEBUG:
        return static_path
    return '{hostname}{static_path}'.format(
        hostname=settings.API_HOSTNAME,
        static_path=static_path,
    )

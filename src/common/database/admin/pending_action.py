# -*- coding: utf-8 -*-

from django.contrib import admin

from src.common.database.models import PendingActionORM


@admin.register(PendingActionORM)
class PendingActiondmin(admin.ModelAdmin):
    """Defines the pending action admin behaviour."""

    search_fields = (
        'uuid',
        'token',
        'tracking_code',
    )
    list_display = (
        'token',
        'tracking_code',
        'category',
        'status',
        'valid_until',
        'metadata',
    )
    list_filter = (
        'category',
        'status',
    )
    raw_id_fields = ('user',)

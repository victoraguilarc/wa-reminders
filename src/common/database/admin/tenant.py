# -*- coding: utf-8 -*-
from django.contrib import admin

from src.common.database.models import TenantORM
from src.common.presentation.utils.admin_widgets import ChoiceDropdownFilter


@admin.register(TenantORM)
class TenantAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    list_display = (
        'slug',
        'name',
        'status',
        'country_iso_code',
        'display_owner',
        'created_at',
    )
    list_filter = (
        'status',
        ('country_iso_code', ChoiceDropdownFilter),
        ('currency_code', ChoiceDropdownFilter),
    )
    raw_id_fields = ('owner', )

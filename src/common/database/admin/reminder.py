# -*- coding: utf-8 -*-
from django.contrib import admin

from src.common.database.models.reminder import ReminderORM, ReminderRecipientORM
from src.common.presentation.utils.admin_widgets import RelatedDropdownFilter


@admin.register(ReminderRecipientORM)
class ReminderRecipientAdmin(admin.ModelAdmin):
    search_fields = ('phone_number__phone_number', )
    list_display = (
        'uuid',
        'status',
        'reminder',
        'phone_number',
    )
    list_filter = (
        'status',
    )
    raw_id_fields = ('reminder', 'phone_number')


class ReminderRecipientInline(admin.TabularInline):
    model = ReminderRecipientORM
    extra = 0
    verbose_name = 'Recipient'
    verbose_name_plural = 'Recipients'
    raw_id_fields = ('phone_number',)



@admin.register(ReminderORM)
class ReminderAdmin(admin.ModelAdmin):
    search_fields = ('scheduled_job_id', 'content')
    inlines = (ReminderRecipientInline,)
    list_display = (
        'uuid',
        'status',
        'scheduled_time',
        'scheduled_job_id',
        'created_at',
    )
    list_filter = (
        ('tenant', RelatedDropdownFilter),
    )
    raw_id_fields = ('tenant', )

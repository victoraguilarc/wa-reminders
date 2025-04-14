# -*- coding: utf-8 -*-

from django.db import models

from src.common.database.models.mixins.tenants import UUIDTimestampTenantMixin
from src.common.domain.enums.tenants import WhatsappSessionStatus


class TenantWhatsappSessionORM(UUIDTimestampTenantMixin):
    session_name = models.CharField(
        verbose_name='Session Name',
        max_length=255,
        db_index=True,
        unique=True,
    )
    phone_number = models.CharField(
        verbose_name='Phone Number',
        help_text='Phone Number of the WhatsApp Account',
        max_length=255,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=50,
        choices=WhatsappSessionStatus.choices(),
        default=str(WhatsappSessionStatus.STARTING),
    )
    messaging_enabled = models.BooleanField(
        verbose_name='Messaging Enabled',
        default=True,
    )
    agents_enabled = models.BooleanField(
        verbose_name='Agents Enabled',
        default=True,
    )
    config = models.JSONField(
        verbose_name='Config',
        help_text='Configuration of the WhatsApp Session',
        default=dict,
        blank=True,
    )

    def __str__(self):
        return self.session_name

    class Meta:
        db_table = 'tenant_whatsapp_sessions'
        verbose_name = 'Tenant WhatsApp Session'
        verbose_name_plural = 'Tenant WhatsApp Session'

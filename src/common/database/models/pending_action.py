# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.db.models import JSONField

from src.common.constants import DEFAULT_PENDING_ACTION_USAGE_LIMIT
from src.common.database.models.mixins.common import UUIDTimestampMixin
from src.common.database.models.mixins.tenants import OptionalTenantMixin
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.helpers.dates import now
from src.common.helpers.enconding import encode_base64


def generate_hex():
    return encode_base64(uuid.uuid4().hex)


class PendingActionORM(OptionalTenantMixin, UUIDTimestampMixin):
    """Represents a user actions that it must be completed."""

    user = models.ForeignKey(
        'UserORM',
        verbose_name='User',
        related_name='pending_actions',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    category = models.CharField(
        verbose_name='Category',
        max_length=50,
        choices=PendingActionCategory.choices(),
        db_index=True,
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=50,
        choices=PendingActionStatus.choices(),
        db_index=True,
        default=str(PendingActionStatus.PENDING),
    )
    token = models.CharField(
        verbose_name='Token',
        max_length=120,
        db_index=True,
        default=generate_hex,
        unique=True,
    )
    tracking_code = models.CharField(
        verbose_name='Tracking Code',
        max_length=120,
        db_index=True,
        default=generate_hex,
        unique=True,
    )
    group_id = models.CharField(
        verbose_name='Group Id',
        max_length=128,
        db_index=True,
        blank=True,
        null=True,
    )
    expired_at = models.DateTimeField(
        verbose_name='Expired At',
        blank=True,
        null=True,
    )
    completed_at = models.DateTimeField(
        verbose_name='Completed At',
        blank=True,
        null=True,
    )
    valid_until = models.DateTimeField(
        verbose_name='Valid Until',
        help_text='The date until the token is valid, null means it never expires',
        blank=True,
        null=True,
    )
    usage_limit = models.PositiveIntegerField(
        verbose_name='Usage Limit',
        default=DEFAULT_PENDING_ACTION_USAGE_LIMIT,
        help_text='How many times the token can be used',
    )
    usage = models.PositiveIntegerField(
        verbose_name='Usage',
        default=0,
        help_text='How many times the token has been used',
    )
    metadata = JSONField(
        verbose_name='Metadata',
        help_text='This field changes according to the type of action',
        default=dict,
        blank=True,
    )

    def expire(self):
        self.status = str(PendingActionStatus.EXPIRED)
        self.expired_at = now()
        self.save(update_fields=['expired_at', 'status'])

    def complete(self):
        self.status = str(PendingActionStatus.COMPLETED)
        self.completed_at = now()
        self.save(update_fields=['completed_at', 'status'])

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'pending_actions'
        verbose_name = 'Pending Action'
        verbose_name_plural = 'Pending Actions'

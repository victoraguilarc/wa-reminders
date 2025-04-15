# -*- coding: utf-8 -*-

import uuid

from django.db import models

from src.common.database.models.mixins.common import UUIDTimestampMixin
from src.common.database.models.mixins.tenants import TenantMixin
from src.common.domain.enums.reminders import ReminderStatus, ReminderRecipientStatus
from src.common.helpers.enconding import encode_base64


def generate_hex():
    return encode_base64(uuid.uuid4().hex)


class ReminderORM(TenantMixin, UUIDTimestampMixin):
    job_id = models.CharField(
        verbose_name='Job ID',
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
    )
    content = models.TextField(
        verbose_name='Content',
        help_text='The content of the reminder',
    )
    scheduled_time = models.DateTimeField(
        verbose_name='Scheduled Time',
        help_text='The time when the reminder should be sent',
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=50,
        choices=ReminderStatus.choices(),
        db_index=True,
        default=str(ReminderStatus.PENDING),
    )

    def __str__(self):
        return self.uuid

    class Meta:
        db_table = 'reminders'
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'


class ReminderRecipientORM(UUIDTimestampMixin):
    reminder = models.ForeignKey(
        'ReminderORM',
        verbose_name='Reminder',
        related_name='recipients',
        on_delete=models.CASCADE,
    )
    phone_number = models.ForeignKey(
        'PhoneNumberORM',
        verbose_name='Phone Number',
        related_name='reminder_recipients',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=50,
        choices=ReminderRecipientStatus.choices(),
        default=str(ReminderRecipientStatus.PENDING),
    )


    def __str__(self):
        return self.uuid

    class Meta:
        db_table = 'reminder_recipients'
        verbose_name = 'Reminder Recipient'
        verbose_name_plural = 'Reminder Recipients'

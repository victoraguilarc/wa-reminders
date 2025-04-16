# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.domain.enums.reminders import ReminderStatus, ReminderRecipientStatus
from src.common.presentation.validators.phone_number import PhoneNumberValidator


class ReminderRecipientValidator(serializers.Serializer):
    phone_number = PhoneNumberValidator()
    status = serializers.ChoiceField(
        choices=ReminderRecipientStatus.choices(),
        required=False,
    )


class CreateReminderValidator(serializers.Serializer):
    content = serializers.CharField()
    scheduled_time = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=ReminderStatus.choices(), required=False)
    recipients = serializers.ListSerializer(
        child=ReminderRecipientValidator(),
        default=[],
    )


class UpdateReminderValidator(serializers.Serializer):
    content = serializers.CharField(required=False)
    scheduled_time = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(
        choices=ReminderStatus.choices(),
        required=False
    )

# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.presentation.validators.phone_number import PhoneNumberValidator
from src.pending_actions.presentation.validators.pending_action import (
    PendingActionRequestValidator,
    PendingActionTokenValidator,
)


class TenantCustomerSessionRedemptionRequestValidator(PendingActionRequestValidator):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = PhoneNumberValidator(required=False, allow_null=True)


class TenantCustomerSessionRedemptionPerformValidator(PendingActionTokenValidator):
    new_password = serializers.CharField()

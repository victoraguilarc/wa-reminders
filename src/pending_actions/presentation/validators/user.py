# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.pending_actions.presentation.validators.pending_action import (
    PendingActionRequestValidator,
    PendingActionTokenValidator,
)


class UserResetPasswordRequestValidator(PendingActionRequestValidator):
    email = serializers.EmailField()


class UserResetPasswordPerformValidator(PendingActionTokenValidator):
    new_password = serializers.CharField()

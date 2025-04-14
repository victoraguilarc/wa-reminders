from rest_framework import serializers

from src.pending_actions.presentation.validators.pending_action import PendingActionRequestValidator


class EmailAddressVerificationRequestValidator(PendingActionRequestValidator):
    email = serializers.EmailField()

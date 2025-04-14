from rest_framework import serializers

from src.common.presentation.validators.simple_person import OptionalPersonValidator
from src.pending_actions.presentation.validators.pending_action import (
    PendingActionTokenValidator,
    PendingActionRequestValidator,
)


class TenantUserInvitationRequestValidator(PendingActionRequestValidator):
    email = serializers.EmailField()


class TenantUserInvitationPerformValidator(PendingActionTokenValidator):
    user_person = OptionalPersonValidator(required=False, allow_null=True)
    accept_invitation = serializers.BooleanField(required=False)

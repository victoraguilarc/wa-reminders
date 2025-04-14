# -*- coding: utf-8 -*-

from rest_framework.request import Request
from rest_framework.response import Response

from src.common.application.responses.generics import TaskResultResponse
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.simple_person import SimplePerson
from src.common.helpers.dicts import validate_mandatory
from src.common.presentation.api.tenant_api import DomainAPIView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.tenant_user.invitation_performer import (
    TenantUserInvitationPerformer,
)
from src.pending_actions.presentation.validators.tenant_user import TenantUserInvitationPerformValidator


class TenantUserInvitationPerformView(DomainAPIView):
    def post(self, request: Request):
        validator = TenantUserInvitationPerformValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        pending_action = PendingActionTokenGetter(
            token=validated_data.get('token'),
            action_repository=self.domain_context.pending_action_repository,
            category=PendingActionCategory.TENANT_USER_INVITATION,
            status=PendingActionStatus.PENDING,
        ).execute()

        TenantUserInvitationPerformer(
            pending_action=pending_action,
            action_repository=self.domain_context.pending_action_repository,
            user_person=(
                SimplePerson.from_dict(validated_data.get('user_person'))
                if validate_mandatory(validated_data, 'user_person')
                else None
            ),
            command_bus=self.bus_context.command_bus,
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

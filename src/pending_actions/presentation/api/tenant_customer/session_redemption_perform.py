# -*- coding: utf-8 -*-

from rest_framework.request import Request
from rest_framework.response import Response

from src.common.application.responses.auth_session import TenantCustomerSessionResponse
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.presentation.api.tenant_api import DomainAPIView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.tenant_customer.session_redemption_performer import (
    TenantCustomerSessionRedemptionPerformer,
)
from src.pending_actions.presentation.validators.pending_action import PendingActionTokenValidator


class TenantCustomerSessionRedemptionPerformView(DomainAPIView):
    def post(self, request: Request):
        validator = PendingActionTokenValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        pending_action = PendingActionTokenGetter(
            token=validated_data.get('token'),
            action_repository=self.domain_context.pending_action_repository,
            category=PendingActionCategory.TENANT_CUSTOMER_SESSION_REDEMPTION,
            status=PendingActionStatus.PENDING,
        ).execute()

        session = TenantCustomerSessionRedemptionPerformer(
            pending_action=pending_action,
            action_repository=self.domain_context.pending_action_repository,
            query_bus=self.bus_context.query_bus,
            command_bus=self.bus_context.command_bus,
        ).execute()

        response = TenantCustomerSessionResponse(instance=session)
        return Response(response.render(self.locale_context))

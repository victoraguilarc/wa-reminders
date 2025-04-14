# -*- coding: utf-8 -*-

from rest_framework.response import Response

from src.common.application.responses.generics import TaskResultResponse
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.presentation.api.tenant_api import DomainAPIView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.email_address.verification_performer import (
    EmailAddressVerificationPerformer,
)
from src.pending_actions.presentation.validators.pending_action import PendingActionTokenValidator


class EmailAddressVerificationPerformView(DomainAPIView):
    def post(self, request):
        validator = PendingActionTokenValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        pending_action = PendingActionTokenGetter(
            token=validated_data.get('token'),
            action_repository=self.domain_context.pending_action_repository,
            category=PendingActionCategory.EMAIL_ADDRESS_VERIFICATION,
            status=PendingActionStatus.PENDING,
        ).execute()

        EmailAddressVerificationPerformer(
            pending_action=pending_action,
            action_repository=self.domain_context.pending_action_repository,
            stream_events_publisher=self.domain_context.stream_events_publisher,
            command_bus=self.bus_context.command_bus,
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

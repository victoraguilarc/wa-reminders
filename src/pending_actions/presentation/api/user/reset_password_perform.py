# -*- coding: utf-8 -*-

from rest_framework.response import Response

from src.common.application.responses.generics import TaskResultResponse
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.presentation.api.tenant_api import DomainAPIView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.user.reset_password_performer import (
    UserResetPasswordPerformer,
)
from src.pending_actions.presentation.validators.user import (
    UserResetPasswordPerformValidator,
)


class UserResetPasswordPerformView(DomainAPIView):
    def post(self, request):
        validator = UserResetPasswordPerformValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        pending_action = PendingActionTokenGetter(
            token=validated_data.get('token'),
            action_repository=self.domain_context.pending_action_repository,
            category=PendingActionCategory.USER_RESET_PASSWORD,
            status=PendingActionStatus.PENDING,
        ).execute()

        UserResetPasswordPerformer(
            pending_action=pending_action,
            new_password=validated_data.get('new_password'),
            action_repository=self.domain_context.pending_action_repository,
            query_bus=self.bus_context.query_bus,
            command_bus=self.bus_context.command_bus,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

# -*- coding: utf-8 -*-
from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.presentation.api.tenant_api import DomainAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.pending_actions.application.use_cases.user.reset_password_generator import (
    UserResetPasswordGenerator,
)
from src.pending_actions.application.use_cases.user.reset_password_notifier import (
    UserResetPasswordNotifier,
)
from src.pending_actions.presentation.api.user.user_action import UserActionView
from src.pending_actions.presentation.validators.user import (
    UserResetPasswordRequestValidator,
)


class UserResetPasswordRequestView(UserActionView, DomainAPIView):
    def post(self, request):
        validator = UserResetPasswordRequestValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        user = self._get_user(email=validated_data.get('email'))
        action_context = UserResetPasswordGenerator(
            user=user,
            action_repository=self.domain_context.pending_action_repository,
            callback_builder=get_composed_callback_builder(
                callback_hostname=validated_data.get('callback_hostname'),
                view_name='views:pending-actions:user-reset-password',
            ),
        ).execute()

        UserResetPasswordNotifier(
            user=user,
            command_bus=self.bus_context.command_bus,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))


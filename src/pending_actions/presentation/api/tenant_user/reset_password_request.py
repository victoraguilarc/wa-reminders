# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.domain.value_objects import TenantUserId
from src.common.presentation.api.tenant_api import RequiredTenantUserAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.pending_actions.application.use_cases.user.reset_password_generator import (
    UserResetPasswordGenerator,
)
from src.pending_actions.application.use_cases.user.reset_password_notifier import (
    UserResetPasswordNotifier,
)
from src.pending_actions.presentation.api.tenant_perms import TenantUserPermissionsMixin
from src.pending_actions.presentation.api.tenant_user.tenant_user_action import (
    TenantUserByIdActionView,
)


class TenantUserResetPasswordRequestByIdView(
    TenantUserPermissionsMixin,
    TenantUserByIdActionView,
    RequiredTenantUserAPIView,
):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_user_id = TenantUserId(kwargs['tenant_user_id'])
        self.validate_tenant_permissions()
        tenant_user = self._get_tenant_user(tenant_user_id=tenant_user_id)

        action_context = UserResetPasswordGenerator(
            user=tenant_user.user,
            action_repository=self.domain_context.pending_action_repository,
            callback_builder=get_composed_callback_builder(
                view_name='views:pending-actions:user-reset-password',
            ),
        ).execute()

        UserResetPasswordNotifier(
            user=tenant_user.user,
            command_bus=self.bus_context.command_bus,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))

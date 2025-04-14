# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.domain.value_objects import TenantUserId
from src.common.presentation.api.tenant_api import RequiredTenantAPIView, RequiredTenantUserAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.pending_actions.application.use_cases.tenant_user.invitation_generator import (
    TenantUserInvitationGenerator,
)
from src.pending_actions.application.use_cases.tenant_user.invitation_notifier import (
    TenantUserInvitationNotifier,
)
from src.pending_actions.presentation.api.tenant_perms import TenantUserPermissionsMixin
from src.pending_actions.presentation.api.tenant_user.tenant_user_action import (
    TenantUserActionView,
    TenantUserByIdActionView,
)
from src.pending_actions.presentation.validators.tenant_user import (
    TenantUserInvitationRequestValidator,
)


class TenantUserInvitationRequestView(TenantUserActionView, RequiredTenantAPIView):
    def post(self, request):
        validator = TenantUserInvitationRequestValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        tenant_user = self._get_tenant_user(email=validated_data.get('email'))
        action_context = TenantUserInvitationGenerator(
            tenant_user=tenant_user,
            action_repository=self.domain_context.pending_action_repository,
            callback_builder=get_composed_callback_builder(
                callback_hostname=validated_data.get('callback_hostname'),
                view_name='views:pending-actions:tenant-user-invitation',
            ),
        ).execute()

        TenantUserInvitationNotifier(
            tenant_user=tenant_user,
            command_bus=self.bus_context.command_bus,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))


class TenantUserInvitationRequestByIdView(
    TenantUserPermissionsMixin,
    TenantUserByIdActionView,
    RequiredTenantUserAPIView,
):

    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_user_id = TenantUserId(kwargs['tenant_user_id'])
        self.validate_tenant_permissions()
        tenant_user = self._get_tenant_user(tenant_user_id=tenant_user_id)

        action_context = TenantUserInvitationGenerator(
            tenant_user=tenant_user,
            action_repository=self.domain_context.pending_action_repository,
            callback_builder=get_composed_callback_builder(
                view_name='views:pending-actions:tenant-user-invitation',
            ),
        ).execute()

        TenantUserInvitationNotifier(
            tenant_user=tenant_user,
            command_bus=self.bus_context.command_bus,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))

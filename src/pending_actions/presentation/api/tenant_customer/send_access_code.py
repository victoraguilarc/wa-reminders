# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.commands.pending_actions import SendTenantCustomerAccessCodeCommand
from src.common.application.responses.generics import TaskResultResponse
from src.common.domain.value_objects import TenantCustomerId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.pending_actions.presentation.api.tenant_customer.tenant_customer_action import (
    TenantCustomerActionByIdView,
)
from src.pending_actions.presentation.api.tenant_perms import TenantUserPermissionsMixin


class TenantCustomerSendAccessCodeView(
    TenantUserPermissionsMixin,
    TenantCustomerActionByIdView,
    RequiredTenantUserAPIView,
):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_customer_id = TenantCustomerId(kwargs['tenant_customer_id'])
        self.validate_tenant_permissions()

        self.bus_context.command_bus.dispatch(
            command=SendTenantCustomerAccessCodeCommand(
                tenant_id=self.tenant_context.tenant.id,
                tenant_customer_id=tenant_customer_id,
            ),
            run_async=not settings.DEBUG,
        )

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.generics import TaskResultResponse
from src.common.application.shortcuts.customers_site import get_members_session_callback_builder
from src.common.domain.value_objects import TenantCustomerId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.common.presentation.api.tenant_api import RequiredTenantAPIView
from src.common.presentation.helpers.phone_number import get_raw_phone_number
from src.pending_actions.application.use_cases.tenant_customer.session_redemption_notifier import (
    TenantCustomerSessionRedemptionNotifier,
)
from src.pending_actions.presentation.api.tenant_customer.tenant_customer_action import (
    TenantCustomerActionView, TenantCustomerActionByIdView,
)
from src.pending_actions.presentation.api.tenant_perms import TenantUserPermissionsMixin
from src.pending_actions.presentation.validators.tenant_customer import (
    TenantCustomerSessionRedemptionRequestValidator,
)


class TenantCustomerSessionRedemptionRequestView(
    TenantCustomerActionView,
    RequiredTenantAPIView,
):
    def post(self, request):
        validator = TenantCustomerSessionRedemptionRequestValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        validated_data = validator.validated_data
        raw_email = validated_data.get('email', None)
        phone_number_data = validated_data.get('phone_number', None)
        raw_phone_number = (
            get_raw_phone_number(phone_number_data)
            if phone_number_data else None
        )

        tenant_customer = self._get_tenant_customer(
            email=raw_email,
            raw_phone_number=raw_phone_number,
        )
        callback_builder = get_members_session_callback_builder(
            query_bus=self.bus_context.query_bus,
            tenant_id=tenant_customer.tenant_id,
        )

        TenantCustomerSessionRedemptionNotifier(
            tenant=self.tenant_context.tenant,
            tenant_customer=tenant_customer,
            command_bus=self.bus_context.command_bus,
            query_bus=self.bus_context.query_bus,
            send_async=not settings.DEBUG,
            callback_builder=callback_builder,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))



class TenantCustomerSessionRedemptionRequestByIdView(
    TenantUserPermissionsMixin,
    TenantCustomerActionByIdView,
    RequiredTenantUserAPIView,
):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_customer_id = TenantCustomerId(kwargs['tenant_customer_id'])
        self.validate_tenant_permissions()
        tenant_customer = self._get_tenant_customer(tenant_customer_id=tenant_customer_id)

        callback_builder = get_members_session_callback_builder(
            query_bus=self.bus_context.query_bus,
            tenant_id=tenant_customer.tenant_id,
        )

        TenantCustomerSessionRedemptionNotifier(
            tenant=self.tenant_context.tenant,
            tenant_customer=tenant_customer,
            command_bus=self.bus_context.command_bus,
            query_bus=self.bus_context.query_bus,
            # send_async=not settings.DEBUG,
            callback_builder=callback_builder,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

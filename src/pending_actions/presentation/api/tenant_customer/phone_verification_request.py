# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.application.shortcuts.customers_site import get_members_callback_builder
from src.common.constants import DEFAULT_PHONE_VERIFICATION_SUB_PATH
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId
from src.common.presentation.api.tenant_api import RequiredTenantUserAPIView
from src.pending_actions.application.use_cases.phone_number.verification_generator import (
    PhoneNumberVerificationGenerator,
)
from src.pending_actions.application.use_cases.phone_number.verification_notifier import (
    PhoneNumberVerificationNotifier,
)
from src.pending_actions.presentation.api.tenant_customer.tenant_customer_action import (
    TenantCustomerActionByIdView,
)
from src.pending_actions.presentation.api.tenant_perms import TenantUserPermissionsMixin


class TenantCustomerPhoneNumberVerificationRequestView(
    TenantUserPermissionsMixin,
    TenantCustomerActionByIdView,
    RequiredTenantUserAPIView,
):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_customer_id = TenantCustomerId(kwargs['tenant_customer_id'])
        self.validate_tenant_permissions()
        tenant_customer: TenantCustomer = self._get_tenant_customer(tenant_customer_id=tenant_customer_id)

        action_context = PhoneNumberVerificationGenerator(
            raw_phone_number=tenant_customer.raw_phone_number,
            action_repository=self.domain_context.pending_action_repository,
            query_bus=self.bus_context.query_bus,
            callback_builder=get_members_callback_builder(
                query_bus=self.bus_context.query_bus,
                tenant_id=tenant_customer.tenant_id,
                sub_path=DEFAULT_PHONE_VERIFICATION_SUB_PATH,
            ),
        ).execute()

        PhoneNumberVerificationNotifier(
            raw_phone_number=tenant_customer.raw_phone_number,
            command_bus=self.bus_context.command_bus,
            lang=self.locale_context.language,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))

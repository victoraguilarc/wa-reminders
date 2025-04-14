# -*- coding: utf-8 -*-
from django.conf import settings

from loguru import logger

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.tenant_customer import TenantCustomerResponse
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.users.application.tenant_customers.use_cases.deleter import TenantCustomerDeleter
from src.users.application.tenant_customers.use_cases.detailer import TenantCustomerDetailer
from src.users.application.tenant_customers.use_cases.updater import TenantCustomerUpdater
from src.users.presentation.validators.tenant_customer import TenantCustomerValidator


class TenantCustomerView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_customer = TenantCustomerDetailer(
            tenant_id=self.tenant_context.tenant.id,
            tenant_customer_id=TenantCustomerId(kwargs.get('tenant_customer_id')),
            repository=self.domain_context.tenant_customer_repository,
        ).execute()

        response = TenantCustomerResponse(tenant_customer)
        return Response(response.render(self.locale_context))

    def put(self, request, **kwargs):
        logger.info(f'request: {request.data}')

        validator = TenantCustomerValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        tenant_customer = TenantCustomerUpdater(
            tenant_id=self.tenant_context.tenant.id,
            tenant_customer_id=TenantCustomerId(kwargs.get('tenant_customer_id')),
            repository=self.domain_context.tenant_customer_repository,
            updated_instance=TenantCustomer.from_payload(validator.validated_data),
            updated_fields=list(validator.validated_data.keys()),
            command_bus=self.bus_context.command_bus,
            run_commands_async=not settings.DEBUG,
        ).execute()

        response = TenantCustomerResponse(tenant_customer)
        return Response(response.render(self.locale_context))

    def delete(self, request, **kwargs):
        app_service = TenantCustomerDeleter(
            tenant_id=self.tenant_context.tenant.id,
            tenant_customer_id=TenantCustomerId(kwargs.get('tenant_customer_id')),
            repository=self.domain_context.tenant_customer_repository,
        )

        response = app_service.execute()
        return Response(
            response.render(self.locale_context),
            status=status.HTTP_204_NO_CONTENT,
        )

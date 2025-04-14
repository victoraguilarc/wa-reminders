# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.common.application.helpers.users import get_customer_creation_source
from src.common.application.presenters.tenant_customer import TenantCustomerPresenter
from src.common.application.responses.pagination import PaginationResponse
from src.common.application.responses.tenant_customer import TenantCustomerResponse
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.enums.users import TenantCustomerStatus
from src.common.infrastructure.query_params import QueryParams
from src.common.presentation.api import RequiredTenantUserAPIView
from src.users.application.tenant_customers.use_cases.creator import TenantCustomerCreator
from src.users.application.tenant_customers.use_cases.lister import TenantCustomersLister
from src.users.domain.filters.tenant_customers import TenantCustomersFilters
from src.users.presentation.validators.tenant_customer import TenantCustomerValidator


class TenantCustomersView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        current_page = TenantCustomersLister(
            tenant_id=self.tenant_context.tenant.id,
            repository=self.domain_context.tenant_customer_repository,
            list_filters=self._get_filters(request),
        ).execute()

        response = PaginationResponse(current_page, TenantCustomerPresenter)
        return Response(response.render(self.locale_context))

    def post(self, request, **kwargs):
        validator = TenantCustomerValidator(
            data=request.data,
            context={'tenant': self.tenant_context.tenant},
        )
        validator.is_valid(raise_exception=True)

        tenant_customer = TenantCustomerCreator(
            tenant_id=self.tenant_context.tenant.id,
            repository=self.domain_context.tenant_customer_repository,
            new_instance=TenantCustomer.from_payload(
                verified_data={
                    **validator.validated_data,
                    'tenant_id': self.tenant_context.tenant.id,
                    'creation_source': str(
                        get_customer_creation_source(self.locale_context.client)
                    ),
                },
            ),
            command_bus=self.bus_context.command_bus,
            run_commands_async=not settings.DEBUG,
        ).execute()

        response = TenantCustomerResponse(instance=tenant_customer)
        return Response(
            response.render(self.locale_context),
            status=status.HTTP_201_CREATED,
        )

    @classmethod
    def _get_filters(cls, request: Request) -> TenantCustomersFilters:
        params = QueryParams(request.query_params)
        return TenantCustomersFilters(
            search_term=params.get_str(key='search', default=None),
            page_size=params.get_int(key='page_size', default=None),
            page_index=params.get_str(key='page_index', default=None),
            statuses=params.get_enum_list(
                key='statuses',
                enum_class=TenantCustomerStatus,
                default=None,
            ),
        )

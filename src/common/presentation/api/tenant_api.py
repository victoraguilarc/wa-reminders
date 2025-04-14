# -*- coding: utf-8 -*-
from typing import Optional

from django.utils import translation
from loguru import logger
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from src.common.domain.context.bus import BusContext
from src.common.domain.context.client import ConsumerClient
from src.common.domain.context.domain import DomainContext
from src.common.domain.context.locale import LocaleContext, TenantContext
from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.entities.user import User
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.locales import Language, TimeZone
from src.common.infrastructure.context_builder import AppContextBuilder
from src.common.infrastructure.django_locales import DjangoLocaleService
from src.common.presentation.api.exceptions.collection import TENANT_ACCESS_UNAUTHORIZED
from src.common.presentation.api.pagination import StandarPagination
from src.common.presentation.api.renderers import StandarJSONRenderer
from src.common.presentation.api.tenant_helpers import (
    get_tenant_customer_from_request,
    get_tenant_from_request,
    get_tenant_user_from_request,
    get_user_from_request,
)
from src.common.presentation.constants import HTTP_CLIENT_HEADER


class DomainAPIView(GenericAPIView):
    """Attach tenant calculationto request > response flow."""

    domain_context: DomainContext = None
    bus_context: BusContext = None
    locale_context: Optional[LocaleContext] = None
    tenant_context: Optional[TenantContext] = None
    user: Optional[User] = None

    format_kwarg = None

    pagination_class = StandarPagination
    renderer_classes = (StandarJSONRenderer,)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.setup_user(request)
        self.check_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)
        self.setup_contexts(request)

    def check_authentication(self, request):
        return

    def render_paginated_response(self, request, items, displayer_class):
        report_items = self.paginator.paginate_queryset(items, request)
        return self.paginator.get_paginated_response(
            displayer_class(report_items, many=True).data,
        )

    def get_tenant_user(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantUser]:
        if not tenant:
            return None
        return get_tenant_user_from_request(request, tenant=tenant)

    def get_tenant_customer(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantUser]:
        return None

    def get_tenant(self, request) -> Optional[Tenant]:
        return get_tenant_from_request(request, tenant_required=False)

    def setup_contexts(
        self,
        request: Request,
    ):
        tenant = self.get_tenant(request)
        country_code = request.query_params.get('countryCode', str(CountryIsoCode.ANY))

        app_context = AppContextBuilder.from_env()

        self.domain_context = app_context.domain
        self.bus_context = app_context.bus

        client_header = request.META.get(HTTP_CLIENT_HEADER, '')
        logger.info(f'Client header: {client_header}')

        self.locale_context = LocaleContext(
            client=ConsumerClient.build(client_header),
            time_zone=tenant.timezone if tenant else TimeZone.UTC,
            language=Language.from_value(translation.get_language()),
            country_config=CountryConfigBuilder.from_iso_code(country_code),
            locale_service=DjangoLocaleService(),
        )
        self.tenant_context = TenantContext(
            tenant=tenant,
            tenant_user=self.get_tenant_user(request, tenant),
            tenant_customer=self.get_tenant_customer(request, tenant),
        )

    def setup_user(self, request):
        self.user = get_user_from_request(request)

    def initialize_request(self, request, *args, **kwargs):
        request: Request = super().initialize_request(request, *args, **kwargs)
        # Add some loggers here
        return request


class RequiredTenantAPIView(DomainAPIView):
    def get_tenant(self, request) -> Optional[Tenant]:
        return get_tenant_from_request(request, tenant_required=True)


class TenantUserAPIView(RequiredTenantAPIView):
    def get_tenant_user(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantUser]:
        if not tenant:
            return None
        return get_tenant_user_from_request(request, tenant=tenant)


class RequiredTenantUserAPIView(RequiredTenantAPIView):
    def get_tenant_user(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantUser]:
        if not tenant:
            return None
        tenant_user = get_tenant_user_from_request(request, tenant=tenant)
        if not tenant_user:
            raise TENANT_ACCESS_UNAUTHORIZED
        return tenant_user


class TenantCustomerAPIView(RequiredTenantAPIView):
    def get_tenant_customer(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantCustomer]:
        if not tenant:
            return None
        return get_tenant_customer_from_request(request, tenant=tenant)


class RequiredTenantCustomerAPIView(RequiredTenantAPIView):
    def get_tenant_customer(
        self,
        request: Request,
        tenant: Optional[Tenant] = None,
    ) -> Optional[TenantCustomer]:
        if not tenant:
            return None
        tenant_customer = get_tenant_customer_from_request(request, tenant=tenant)
        if not tenant_customer:
            raise TENANT_ACCESS_UNAUTHORIZED
        return tenant_customer

# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from src.common.domain.enums.tenants import LinkedSiteCategory
from src.common.presentation.api import DomainAPIView
from src.tenants.application.tenants.responses import TenantResponse
from src.tenants.application.tenants.use_cases.getter import TenantFromSiteGetter
from src.tenants.application.tenants.use_cases.wa_session_getter import TenantFromWhatsappSessionGetter
from src.tenants.application.whatsapp_sessions.responses import AgentTenantWhatsappSessionResponse
from src.tenants.presentation.validators.tenant import TenantFromSiteValidator, TenantFromWhatsappSessionValidator


class TenantFromSiteView(DomainAPIView):
    permission_classes = (HasAPIKey,)

    def post(self, request, **kwargs):
        validator = TenantFromSiteValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        tenant_container = TenantFromSiteGetter(
            domain=validator.validated_data['domain'],
            category=LinkedSiteCategory.from_value(validator.validated_data['category']),
            query_bus=self.bus_context.query_bus,
            tenant_repository=self.domain_context.tenant_repository,
            include_resources=validator.validated_data.get('include_resources', False),
        ).execute()

        response = TenantResponse(tenant_container)
        return Response(response.render(self.locale_context))


class TenantFromWhatsappSessionView(DomainAPIView):
    permission_classes = (HasAPIKey,)

    def post(self, request, **kwargs):
        validator = TenantFromWhatsappSessionValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        tenant_wa_session = TenantFromWhatsappSessionGetter(
            session_name=validator.validated_data['session_name'],
            repository=self.domain_context.tenant_repository,
        ).execute()

        response = AgentTenantWhatsappSessionResponse(tenant_wa_session)
        return Response(response.render(self.locale_context))

# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from src.common.presentation.api import DomainAPIView
from src.tenants.application.tenants.use_cases.wa_session_getter import TenantFromWhatsappSessionGetter
from src.tenants.application.whatsapp_sessions.responses import AgentTenantWhatsappSessionResponse
from src.tenants.presentation.validators.tenant import TenantFromWhatsappSessionValidator


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

# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.presentation.api import PaginationMixin, RequiredTenantUserAPIView
from src.tenants.application.whatsapp_sessions.responses import (
    TenantWhatsappSessionsResponse,
    TenantWhatsappSessionResponse,
)
from src.tenants.application.whatsapp_sessions.use_cases.creator import TenantWhatsappSessionCreator
from src.tenants.application.whatsapp_sessions.use_cases.lister import TenantWhatsappSessionsLister
from src.tenants.infrastructure.whatsapp.webhooks import get_whatsapp_webhooks


class TenantWhatsappSessionsView(PaginationMixin, RequiredTenantUserAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        instances = TenantWhatsappSessionsLister(
            tenant_id=self.tenant_context.tenant.id,
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
            force_refresh=True,
        ).execute()

        response = TenantWhatsappSessionsResponse(instances)
        return self.paginated_response(
            request,
            response.render(self.locale_context),
        )

    def post(self, request, **kwargs):
        instance = TenantWhatsappSessionCreator(
            tenant=self.tenant_context.tenant,
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
            session_webhooks=get_whatsapp_webhooks(),
        ).execute()

        response = TenantWhatsappSessionResponse(instance)
        return Response(
            response.render(self.locale_context),
            status=status.HTTP_201_CREATED,
        )

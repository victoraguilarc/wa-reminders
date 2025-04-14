# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.presentation.api.tenant_api import RequiredTenantUserAPIView


class TenantUserSessionConfigView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):

        session_config = TenantSessionConfigBuilder(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=self.tenant_context.tenant_user.id,
            repository=self.domain_context.tenant_user_repository,
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = TenantSessionConfigResponse(instance=session_config)
        return Response(response.render(self.locale_context))

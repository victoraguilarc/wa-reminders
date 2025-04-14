# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.presenters.tenant import TenantPresenter
from src.common.domain.models.tenant import Tenant
from src.common.presentation.api import DomainAPIView
from src.tenants.application.tenants.responses import TenantResponse
from src.tenants.presentation.validators.tenant import CreateTenantValidator


class TenantsView(DomainAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        validator = CreateTenantValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        tenant = Tenant.build_from_payload(validator.validated_data)

        response = TenantResponse(tenant)
        return Response(response.render(self.locale_context))

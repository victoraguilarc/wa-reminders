# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.value_objects import TenantWhatsappSessionId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.tenants.application.whatsapp_sessions.responses import TenantWhatsappSessionResponse, \
    TenantWhatsappSessionQRCodeResponse
from src.tenants.application.whatsapp_sessions.use_cases.deleter import TenantWhatsappSessionDeleter
from src.tenants.application.whatsapp_sessions.use_cases.detailer import TenantWhatsappSessionDetailer
from src.tenants.application.whatsapp_sessions.use_cases.patcher import TenantWhatsappSessionPatcher
from src.tenants.application.whatsapp_sessions.use_cases.qrcode_getter import TenantWhatsappSessionQRCodeGetter
from src.tenants.application.whatsapp_sessions.use_cases.updater import TenantWhatsappSessionUpdater
from src.tenants.presentation.validators.tenant_wa_session import WhatsappSessionPatchValidator


class TenantWhatsappSessionView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        instance = TenantWhatsappSessionDetailer(
            tenant_id=self.tenant_context.tenant.id,
            instance_id=TenantWhatsappSessionId(kwargs.get('whatsapp_session_id')),
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
        ).execute()

        response = TenantWhatsappSessionResponse(instance)
        return Response(response.render(self.locale_context))

    def put(self, request, **kwargs):
        instance = TenantWhatsappSessionUpdater(
            tenant_id=self.tenant_context.tenant.id,
            instance_id=TenantWhatsappSessionId(kwargs.get('whatsapp_session_id')),
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
        ).execute()

        response = TenantWhatsappSessionResponse(instance)
        return Response(response.render(self.locale_context))

    def patch(self, request, **kwargs):

        validator = WhatsappSessionPatchValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        instance = TenantWhatsappSessionPatcher(
            tenant_id=self.tenant_context.tenant.id,
            instance_id=TenantWhatsappSessionId(kwargs.get('whatsapp_session_id')),
            updated_properties=validator.validated_data,
            repository=self.domain_context.whatsapp_session_repository,
        ).execute()

        response = TenantWhatsappSessionResponse(instance)
        return Response(response.render(self.locale_context))

    def delete(self, request, **kwargs):
        TenantWhatsappSessionDeleter(
            tenant_id=self.tenant_context.tenant.id,
            instance_id=TenantWhatsappSessionId(kwargs.get('whatsapp_session_id')),
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
        ).execute()

        response = TenantWhatsappSessionResponse()
        return Response(
            response.render(self.locale_context),
            status=status.HTTP_204_NO_CONTENT,
        )


class TenantWhatsappSessionQRCodeView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        instance = TenantWhatsappSessionQRCodeGetter(
            tenant_id=self.tenant_context.tenant.id,
            instance_id=TenantWhatsappSessionId(kwargs.get('whatsapp_session_id')),
            repository=self.domain_context.whatsapp_session_repository,
            session_manager=self.domain_context.whatsapp_session_manager,
        ).execute()

        response = TenantWhatsappSessionQRCodeResponse(instance)
        return Response(response.render(self.locale_context))

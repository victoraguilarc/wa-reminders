# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from src.common.application.responses.generics import TaskResultResponse
from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.presentation.api import DomainAPIView
from src.tenants.application.whatsapp_sessions.use_cases.status_updater import (
    WhatsappSessionStatusUpdater,
)
from src.tenants.presentation.validators.tenant_wa_session import (
    WhatsappSessionStatusPayloadValidator,
)


class TenantWhatsappSessionStatusWebhookView(DomainAPIView):
    permission_classes = (HasAPIKey,)

    def post(self, request, **kwargs):
        validator = WhatsappSessionStatusPayloadValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        payload = validator.validated_data['payload']

        WhatsappSessionStatusUpdater(
            session_name=payload['name'],
            repository=self.domain_context.whatsapp_session_repository,
            status=WhatsappSessionStatus.from_value(payload['status']),
            stream_events_publisher=self.domain_context.stream_events_publisher,
            session_manager=self.domain_context.whatsapp_session_manager,
        ).execute()

        response = TaskResultResponse()
        return Response(response.render(self.locale_context))

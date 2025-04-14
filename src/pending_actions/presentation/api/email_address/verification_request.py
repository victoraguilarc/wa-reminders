# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.presentation.api.tenant_api import DomainAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.pending_actions.application.use_cases.email_address.verification_generator import (
    EmailAddressVerificationGenerator,
)
from src.pending_actions.application.use_cases.email_address.verification_notifier import (
    EmailAddressVerificationNotifier,
)
from src.pending_actions.presentation.validators.email_address import (
    EmailAddressVerificationRequestValidator,
)


class EmailAddressVerificationRequestView(DomainAPIView):
    def post(self, request):
        validator = EmailAddressVerificationRequestValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        raw_email = validated_data.get('email')
        action_context = EmailAddressVerificationGenerator(
            email=raw_email,
            action_repository=self.domain_context.pending_action_repository,
            query_bus=self.bus_context.query_bus,
            callback_builder=get_composed_callback_builder(
                callback_hostname=validated_data.get('callback_hostname'),
                view_name='views:pending-actions:email-address-verification',
            ),
        ).execute()

        EmailAddressVerificationNotifier(
            email=raw_email,
            command_bus=self.bus_context.command_bus,
            callback_url=action_context.callback_url,
            send_async_email=not settings.DEBUG,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))


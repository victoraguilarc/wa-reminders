# -*- coding: utf-8 -*-

from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.presentation.api.tenant_api import DomainAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.common.presentation.helpers.phone_number import get_raw_phone_number
from src.common.presentation.validators.phone_number import PhoneNumberValidator
from src.pending_actions.application.use_cases.phone_number.verification_generator import (
    PhoneNumberVerificationGenerator,
)
from src.pending_actions.application.use_cases.phone_number.verification_notifier import (
    PhoneNumberVerificationNotifier,
)


class PhoneNumberVerificationRequestView(DomainAPIView):
    def post(self, request):
        validator = PhoneNumberValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        raw_phone_number = get_raw_phone_number(validated_data)
        action_context = PhoneNumberVerificationGenerator(
            raw_phone_number=raw_phone_number,
            action_repository=self.domain_context.pending_action_repository,
            query_bus=self.bus_context.query_bus,
            callback_builder=get_composed_callback_builder(
                callback_hostname=validated_data.get('callback_hostname'),
                view_name='views:pending-actions:phone-number-verification',
            ),
        ).execute()

        PhoneNumberVerificationNotifier(
            raw_phone_number=raw_phone_number,
            command_bus=self.bus_context.command_bus,
            lang=self.locale_context.language,
            callback_url=action_context.callback_url,
        ).execute()

        response = PendingActionResponse(action_context.pending_action)
        return Response(response.render(self.locale_context))

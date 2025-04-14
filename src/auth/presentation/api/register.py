# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.response import Response

from src.auth.application.use_cases.user_register import UserRegister
from src.auth.presentation.validators.session_user import CreateUserValidator
from src.common.application.responses.pending_action import PendingActionResponse
from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.user import User
from src.common.presentation.api.tenant_api import DomainAPIView
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder


class RegisterView(DomainAPIView):
    def post(self, request):
        validator = CreateUserValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        pending_action = UserRegister(
            user_instance=User.from_payload(
                verified_data=validator.validated_data,
                email_address=EmailAddress.from_dict(validator.validated_data),
            ),
            raw_password=validator.validated_data.get('password'),
            session_user_repository=self.domain_context.session_user_repository,
            query_bus=self.bus_context.query_bus,
            callback_builder=get_composed_callback_builder(
                view_name='views:pending-actions:email-address-verification',
            ),
            send_async_email=not settings.DEBUG,
        ).execute()

        response = PendingActionResponse(instance=pending_action)
        return Response(
            response.render(self.locale_context),
        )

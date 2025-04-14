# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response

from src.auth.application.use_cases.session_builder import LoginSessionBuilder
from src.auth.presentation.validators.login import LoginValidator
from src.common.application.responses.auth_session import TenantUserSessionResponse
from src.common.presentation.api.tenant_api import DomainAPIView


class LoginView(DomainAPIView):
    def post(self, request: Request):
        validator = LoginValidator(
            data=request.data,
            context={'request': request},
        )
        validator.is_valid(raise_exception=True)

        session = LoginSessionBuilder(
            email=validator.validated_data.get('email'),
            password=validator.validated_data.get('password'),
            session_repository=self.domain_context.session_repository,
            query_bus=self.bus_context.query_bus,
            path_hostname=settings.BACKOFFICE_HOSTNAME,
        ).execute()

        response = TenantUserSessionResponse(session)
        return Response(
            response.render(self.locale_context),
        )

# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.auth.application.use_cases.session_detailer import UserSessionDetailer
from src.common.application.responses.auth_session import TenantUserSessionResponse
from src.common.domain.value_objects import UserId
from src.common.presentation.api.tenant_api import DomainAPIView


# TODO: deprecate this in favor to session config
class SessionView(DomainAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):

        session = UserSessionDetailer(
            user_id=UserId(request.user.uuid),
            user_repository=self.domain_context.user_repository,
            session_repository=self.domain_context.session_repository,
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = TenantUserSessionResponse(session)
        return Response(
            response.render(self.locale_context),
        )

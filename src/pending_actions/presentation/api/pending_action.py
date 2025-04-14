# -*- coding: utf-8 -*-

from rest_framework.response import Response

from src.common.application.responses.pending_action import PendingActionResponse
from src.common.presentation.api.tenant_api import DomainAPIView
from src.pending_actions.application.use_cases.action_getter import PendingActionGetter


class PendingActionView(DomainAPIView):
    def get(self, request, *args, **kwargs):
        tracking_code = kwargs.get('token_or_tracking_code')

        pending_action = PendingActionGetter(
            token_or_tracking_code=tracking_code,
            action_repository=self.domain_context.pending_action_repository,
        ).execute()

        response = PendingActionResponse(pending_action)
        return Response(response.render(self.locale_context))

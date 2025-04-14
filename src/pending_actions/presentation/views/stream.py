# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
# from django_grip import set_hold_stream
from djangorestframework_camel_case.util import camelize
from rest_framework import status

from src.common.helpers.dates import now
from src.common.presentation.views.stream_view import StreamView
from src.pending_actions.application.use_cases.action_getter import PendingActionGetter
from src.pending_actions.application.use_cases.update_publisher import (
    PendingActionSSEventPublisher,
)


class PendingActionStream(StreamView):
    def get(self, request, **kwargs):
        tracking_code = kwargs.get('tracking_code')

        pending_action = PendingActionGetter(
            token_or_tracking_code=tracking_code,
            action_repository=self.domain_context.pending_action_repository,
        ).execute()

        if request.grip_proxied:
            # set_hold_stream(request, pending_action.channel_id)
            return HttpResponse(content_type='text/event-stream')

        return JsonResponse(
            data=camelize(
                self._build_response(pending_action.to_tracking_dict),
            ),
        )

    def post(self, request, **kwargs):
        tracking_code = kwargs.get('tracking_code')

        pending_action = PendingActionGetter(
            token_or_tracking_code=tracking_code,
            action_repository=self.domain_context.pending_action_repository,
        ).execute()

        PendingActionSSEventPublisher(
            pending_action=pending_action,
            stream_events_publisher=self.domain_context.stream_events_publisher,
        ).execute()

        return JsonResponse(
            data=camelize(
                self._build_response(pending_action.to_tracking_dict),
            ),
            status=status.HTTP_201_CREATED,
        )

    @classmethod
    def _build_response(cls, data: dict):
        return {
            'data': data,
            'datetime': str(now()),
        }

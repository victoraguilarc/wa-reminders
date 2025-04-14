# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.value_objects import NotificationId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.notifications.application.notifications.finder import NotificationFinder


class NotificationView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        app_service = NotificationFinder(
            tenant_id=self.tenant_context.tenant.id,
            notification_id=NotificationId(kwargs.get('notification_id')),
            notification_repository=self.domain_context.notification_repository,
        )

        response = app_service.execute()
        return Response(response.render(self.locale_context))

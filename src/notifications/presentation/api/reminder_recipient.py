# -*- coding: utf-8 -*-
from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.presentation.api import RequiredTenantUserAPIView
from src.notifications.application.reminder_recipients.use_cases.deleter import ReminderRecipientDeleter


class ReminderRecipientView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, reminder_id: UUID, reminder_recipient_id: UUID):
        ReminderRecipientDeleter(
            reminder_id=reminder_id,
            reminder_recipient_id=reminder_recipient_id,
            repository=self.domain_context.reminder_repository,
        ).execute()

        return Response(data="", status=204)

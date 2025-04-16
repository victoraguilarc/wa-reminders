# -*- coding: utf-8 -*-
from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.enums.reminders import ReminderRecipientStatus
from src.common.presentation.api import RequiredTenantUserAPIView
from src.notifications.application.reminder_recipients.use_cases.creator import ReminderRecipientCreator
from src.notifications.presentation.api.responses.reminder import ReminderResponse
from src.notifications.presentation.api.validators.reminder import ReminderRecipientValidator


class ReminderRecipientsView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, reminder_id: UUID):
        validator = ReminderRecipientValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        reminder = ReminderRecipientCreator(
            tenant_id=self.tenant_context.tenant.id,
            reminder_id=reminder_id,
            repository=self.domain_context.reminder_repository,
            status=ReminderRecipientStatus.from_value(validated_data.get("status")),
            phone_number_data=validated_data.get("phone_number", {}),
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = ReminderResponse(instance=reminder)
        return Response(response.render(self.locale_context))


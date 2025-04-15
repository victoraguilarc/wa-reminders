# -*- coding: utf-8 -*-
import uuid

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.reminder import ReminderRecipient
from src.common.domain.enums.reminders import ReminderStatus, ReminderRecipientStatus
from src.common.domain.value_objects import ReminderRecipientId, PhoneNumberId
from src.common.presentation.api import PaginationMixin, RequiredTenantUserAPIView
from src.notifications.application.reminders.use_cases.creator import ReminderCreator
from src.notifications.application.reminders.use_cases.lister import RemiderLister
from src.notifications.infrastructure.tasks.reminders import create_reminder_job
from src.notifications.presentation.api.responses.reminder import RemindersResponse, ReminderResponse
from src.notifications.presentation.api.validators.reminder import CreateReminderValidator


class RemindersView(PaginationMixin, RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        reminders = RemiderLister(
            tenant_id=self.tenant_context.tenant.id,
            repository=self.domain_context.reminder_repository,
        ).execute()

        response = RemindersResponse(instances=reminders)
        return Response(response.render(self.locale_context))


    def post(self, request, **kwargs):
        validator = CreateReminderValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        reminder = ReminderCreator(
            tenant_id=self.tenant_context.tenant.id,
            content=validated_data["content"],
            scheduled_time=validated_data["scheduled_time"],
            status=ReminderStatus.from_value(validated_data.get("status")),
            job_scheduler=create_reminder_job,
            repository=self.domain_context.reminder_repository,
            recipients=[
                ReminderRecipient(
                    id=ReminderRecipientId(uuid.uuid4()),
                    phone_number=PhoneNumber.from_dict({
                        "id": PhoneNumberId(uuid.uuid4()),
                        **recipient_data.get("phone_number", {}),
                    }),
                    status=ReminderRecipientStatus.from_value(recipient_data.get("status")),
                )
                for recipient_data in validated_data.get("recipients", [])
            ],
        ).execute()

        response = ReminderResponse(instance=reminder)
        return Response(response.render(self.locale_context))

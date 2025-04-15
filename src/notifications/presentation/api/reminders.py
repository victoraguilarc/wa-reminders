# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.enums.reminders import ReminderStatus
from src.common.presentation.api import RequiredTenantUserAPIView
from src.notifications.application.reminders.use_cases.creator import ReminderCreator
from src.notifications.application.reminders.use_cases.lister import RemiderLister
from src.notifications.application.reminders.use_cases.recipients_builder import RecipientsBuilder
from src.notifications.infrastructure.tasks.reminders import create_reminder_job
from src.notifications.presentation.api.responses.reminder import RemindersResponse, ReminderResponse
from src.notifications.presentation.api.validators.reminder import CreateReminderValidator


class RemindersView(RequiredTenantUserAPIView):
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

        recipients = RecipientsBuilder(
            recipients_data=validated_data.get("recipients", []),
            query_bus=self.bus_context.query_bus,
        ).execute()

        reminder = ReminderCreator(
            tenant_id=self.tenant_context.tenant.id,
            content=validated_data["content"],
            scheduled_time=validated_data["scheduled_time"],
            status=ReminderStatus.from_value(validated_data.get("status")),
            job_scheduler=create_reminder_job,
            repository=self.domain_context.reminder_repository,
            recipients=recipients,
        ).execute()

        response = ReminderResponse(instance=reminder)
        return Response(response.render(self.locale_context))


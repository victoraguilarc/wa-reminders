# -*- coding: utf-8 -*-
from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.presentation.api import RequiredTenantUserAPIView
from src.notifications.application.reminders.use_cases.deleter import ReminderDeleter
from src.notifications.application.reminders.use_cases.finder import ReminderFinder
from src.notifications.application.reminders.use_cases.updater import ReminderUpdater
from src.notifications.infrastructure.tasks.reminders import update_reminder_job, cancel_reminder_job
from src.notifications.presentation.api.responses.reminder import ReminderResponse
from src.notifications.presentation.api.validators.reminder import UpdateReminderValidator


class ReminderView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, reminder_id: UUID):
        reminder = ReminderFinder(
            reminder_id=reminder_id,
            repository=self.domain_context.reminder_repository,
        ).execute()

        response = ReminderResponse(instance=reminder)
        return Response(response.render(self.locale_context))

    def put(self, request, reminder_id: UUID):
        validator = UpdateReminderValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        reminder = ReminderUpdater(
            reminder_id=reminder_id,
            repository=self.domain_context.reminder_repository,
            validated_data=validated_data,
            job_updater=update_reminder_job,
        ).execute()

        response = ReminderResponse(instance=reminder)
        return Response(response.render(self.locale_context))

    def delete(self, request, reminder_id: UUID):
        ReminderDeleter(
            reminder_id=reminder_id,
            repository=self.domain_context.reminder_repository,
            job_canceller=cancel_reminder_job,
        ).execute()

        return Response(data="", status=204)

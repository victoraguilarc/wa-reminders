from dataclasses import dataclass
from typing import Callable

from src.common.application.helpers.props import overload_properties
from src.common.domain.entities.reminder import Reminder
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import ReminderId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderUpdater(GetReminderMixin, UseCase):
    reminder_id: ReminderId
    repository: ReminderRepository
    validated_data: dict[str, any]
    job_updater: Callable[[Reminder], str]

    def execute(self, *args, **kwargs):
        reminder = self.get_reminder(reminder_id=self.reminder_id)

        overload_properties(
            instance=reminder,
            validated_data=self.validated_data,
        )

        reminder.job_id = self.job_updater(reminder)
        return self.repository.persist(instance=reminder)



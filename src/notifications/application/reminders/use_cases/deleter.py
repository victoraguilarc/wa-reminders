from dataclasses import dataclass
from typing import Callable

from src.common.domain.entities.reminder import Reminder
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import ReminderId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderDeleter(GetReminderMixin, UseCase):
    reminder_id: ReminderId
    repository: ReminderRepository
    job_canceller: Callable[[Reminder], None]

    def execute(self):
        reminder = self.get_reminder(reminder_id=self.reminder_id)
        self.job_canceller(reminder)
        self.repository.delete(instance_id=reminder.id)

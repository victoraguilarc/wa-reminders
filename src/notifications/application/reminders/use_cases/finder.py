from dataclasses import dataclass

from src.common.domain.entities.reminder import Reminder
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import ReminderId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderFinder(GetReminderMixin, UseCase):
    reminder_id: ReminderId
    repository: ReminderRepository

    def execute(self) -> Reminder:
        return self.get_reminder(reminder_id=self.reminder_id)

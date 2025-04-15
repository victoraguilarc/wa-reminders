from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.reminder import Reminder
from src.common.domain.value_objects import ReminderId
from src.notifications.domain.exceptions import ReminderNotFoundError
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class GetReminderMixin(object):
    reminder_id: ReminderId
    repository: ReminderRepository

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        reminder = self.repository.find(instance_id=reminder_id)
        if not reminder:
            raise ReminderNotFoundError
        return reminder

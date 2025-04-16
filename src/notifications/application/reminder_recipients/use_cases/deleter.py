from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import ReminderId, ReminderRecipientId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderRecipientDeleter(GetReminderMixin, UseCase):
    reminder_id: ReminderId
    reminder_recipient_id: ReminderRecipientId
    repository: ReminderRepository

    def execute(self):
        self.get_reminder(reminder_id=self.reminder_id)
        self.repository.delete_recipient(instance_id=self.reminder_recipient_id)

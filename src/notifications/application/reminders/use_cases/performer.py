from dataclasses import dataclass

from src.common.domain.entities.whatsapp_message import TextWhatsappMessage
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import ReminderId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin
from src.notifications.domain.interfaces.whatsapp_sender import WhatsappSender
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderPerformer(GetReminderMixin, UseCase):
    reminder_id: ReminderId
    repository: ReminderRepository
    whatsapp_sender: WhatsappSender
    whatsapp_session: str

    def execute(self):
        reminder = self.get_reminder(reminder_id=self.reminder_id)

        if not reminder.recipients:
            return None

        for recipient in reminder.recipients:
            self.whatsapp_sender.send_message(
                phone_number=recipient.phone_number.international_number,
                message=TextWhatsappMessage(content=reminder.content),
                session_name=self.whatsapp_session,
            )



from dataclasses import dataclass
from typing import Optional
from venv import logger

from src.common.domain.entities.reminder import Reminder, ReminderRecipient
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
        reminder: Optional[Reminder] = self.get_reminder(reminder_id=self.reminder_id)

        if not reminder:
            logger.warning("Reminder not found: ", reminder.id)
            return

        pending_recipients = [
            recipient
            for recipient in reminder.recipients
            if recipient.status.is_pending
        ]

        if not pending_recipients:
            logger.warning("No pending recipients found: %s", reminder.id)
            return

        try:
            reminder.in_progress()
            self.repository.persist(reminder, persist_recipients=False)

            recipient: ReminderRecipient
            for recipient in pending_recipients:
                self.whatsapp_sender.send_message(
                    phone_number=recipient.phone_number.international_number,
                    message=TextWhatsappMessage(content=reminder.content),
                    session_name=self.whatsapp_session,
                )
                recipient.sent()
                self.repository.persist_recipient(reminder.id, recipient)

            reminder.completed()
            self.repository.persist(reminder, persist_recipients=False)

        except Exception as exc:
            reminder.failed()
            self.repository.persist(reminder, persist_recipients=False)
            raise exc




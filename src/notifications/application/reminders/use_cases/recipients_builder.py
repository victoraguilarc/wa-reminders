import uuid
from dataclasses import dataclass

from src.common.domain.entities.reminder import ReminderRecipient
from src.common.domain.enums.reminders import ReminderRecipientStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import ReminderRecipientId
from src.notifications.application.reminders.use_cases.mixins import BuildPhoneNumberMixin


@dataclass
class RecipientsBuilder(BuildPhoneNumberMixin, UseCase):
    recipients_data: list[dict]
    query_bus: QueryBus

    def execute(self) -> list[ReminderRecipient]:
        return [
            ReminderRecipient(
                id=ReminderRecipientId(uuid.uuid4()),
                phone_number=self.build_phone_number(recipient_data.get("phone_number", {})),
                status=ReminderRecipientStatus.from_value(recipient_data.get("status")),
            )
            for recipient_data in self.recipients_data
        ]



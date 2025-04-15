import uuid
from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import GetOrCreatePhoneNumberQuery
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.reminder import ReminderRecipient
from src.common.domain.enums.reminders import ReminderRecipientStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import ReminderRecipientId, PhoneNumberId, RawPhoneNumber


@dataclass
class RecipientsBuilder(UseCase):
    recipients_data: list[dict]
    query_bus: QueryBus

    def execute(self) -> list[ReminderRecipient]:
        return [
            ReminderRecipient(
                id=ReminderRecipientId(uuid.uuid4()),
                phone_number=self._build_phone_number(recipient_data.get("phone_number", {})),
                status=ReminderRecipientStatus.from_value(recipient_data.get("status")),
            )
            for recipient_data in self.recipients_data
        ]

    def _build_phone_number(self, phone_number_data) -> Optional[PhoneNumber]:
        phone_number: Optional[PhoneNumber] = self.query_bus.ask(
            query=GetOrCreatePhoneNumberQuery(
                raw_phone_number=RawPhoneNumber.from_dict(phone_number_data),
            ),
        )
        return phone_number

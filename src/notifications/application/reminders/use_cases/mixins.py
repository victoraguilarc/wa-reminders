from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import GetOrCreatePhoneNumberQuery
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.reminder import Reminder
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import ReminderId, RawPhoneNumber
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


@dataclass
class BuildPhoneNumberMixin(object):
    query_bus: QueryBus

    def build_phone_number(self, phone_number_data: dict) -> Optional[PhoneNumber]:
        phone_number: Optional[PhoneNumber] = self.query_bus.ask(
            query=GetOrCreatePhoneNumberQuery(
                raw_phone_number=RawPhoneNumber.from_dict(phone_number_data),
            ),
        )
        return phone_number

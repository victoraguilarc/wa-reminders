import uuid
from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.reminder import ReminderRecipient
from src.common.domain.enums.reminders import ReminderRecipientStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import TenantId, ReminderRecipientId, ReminderId
from src.notifications.application.reminders.use_cases.mixins import GetReminderMixin, BuildPhoneNumberMixin
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderRecipientCreator(BuildPhoneNumberMixin, GetReminderMixin, UseCase):
    tenant_id: TenantId
    reminder_id: ReminderId
    repository: ReminderRepository
    query_bus: QueryBus
    phone_number_data: dict
    status: Optional[ReminderRecipientStatus] = ReminderRecipientStatus.PENDING


    def execute(self):
        reminder = self.get_reminder(self.reminder_id)
        return self.repository.persist_recipient(
            reminder_id=reminder.id,
            instance=ReminderRecipient(
                id=ReminderRecipientId(uuid.uuid4()),
                status=self.status,
                phone_number=self.build_phone_number(self.phone_number_data),
            ),
        )

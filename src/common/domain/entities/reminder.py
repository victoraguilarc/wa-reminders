from dataclasses import dataclass
from datetime import datetime

from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.enums.reminders import ReminderRecipientStatus, ReminderStatus
from src.common.domain.value_objects import TenantId, ReminderRecipientId, ReminderId


@dataclass
class ReminderRecipient(object):
    id: ReminderId
    phone_number: PhoneNumber
    status: ReminderRecipientStatus



@dataclass
class Reminder(object):
    id: ReminderRecipientId
    tenant_id: TenantId
    content: str
    scheduled_time: datetime
    status: ReminderStatus
    recipients: list[ReminderRecipient] = None

    def __post_init__(self):
        self.recipients = self.recipients or []


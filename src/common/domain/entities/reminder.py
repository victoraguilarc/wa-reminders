from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.enums.reminders import ReminderRecipientStatus, ReminderStatus
from src.common.domain.value_objects import TenantId, ReminderRecipientId, ReminderId


@dataclass
class ReminderRecipient(object):
    id: ReminderId
    phone_number: PhoneNumber
    status: ReminderRecipientStatus

    def sent(self):
        self.status = ReminderRecipientStatus.SENT

    def failed(self):
        self.status = ReminderRecipientStatus.FAILED

@dataclass
class Reminder(object):
    id: ReminderRecipientId
    tenant_id: TenantId
    content: str
    scheduled_time: datetime
    status: ReminderStatus
    scheduled_job_id: Optional[str] = None
    recipients: list[ReminderRecipient] = None

    def pending(self):
        self.status = ReminderStatus.PENDING

    def enqueued(self):
        self.status = ReminderStatus.ENQUEUED

    def in_progress(self):
        self.status = ReminderStatus.IN_PROGRESS

    def completed(self):
        self.status = ReminderStatus.COMPLETED

    def failed(self):
        self.status = ReminderStatus.FAILED

    def __post_init__(self):
        self.recipients = self.recipients or []


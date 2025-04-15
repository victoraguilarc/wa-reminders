import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from src.common.domain.entities.reminder import Reminder, ReminderRecipient
from src.common.domain.enums.reminders import ReminderStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId, ReminderRecipientId
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class ReminderCreator(UseCase):
    tenant_id: TenantId
    repository: ReminderRepository
    content: str
    scheduled_time: datetime
    status: ReminderStatus
    job_scheduler: Callable[[Reminder], str]
    recipients: list[ReminderRecipient] = None

    def execute(self):
        reminder = self.repository.persist(
            instance=Reminder(
                id=ReminderRecipientId(uuid.uuid4()),
                tenant_id=self.tenant_id,
                content=self.content,
                scheduled_time=self.scheduled_time,
                status=self.status,
                recipients=self.recipients or [],
            ),
        )
        reminder.scheduled_job_id = self.job_scheduler(reminder)
        return self.repository.persist(instance=reminder)

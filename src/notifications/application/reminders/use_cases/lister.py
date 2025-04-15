from dataclasses import dataclass

from src.common.domain.entities.reminder import Reminder
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId
from src.notifications.domain.repositories.reminder import ReminderRepository


@dataclass
class RemiderLister(UseCase):
    tenant_id: TenantId
    repository: ReminderRepository

    def execute(self) -> list[Reminder]:
        return self.repository.filter(tenant_id=self.tenant_id)

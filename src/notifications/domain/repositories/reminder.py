# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.entities.reminder import Reminder, ReminderRecipient
from src.common.domain.value_objects import ReminderId, TenantId, ReminderRecipientId


class ReminderRepository(ABC):
    @abstractmethod
    def find(self, instance_id: ReminderId) -> Optional[Reminder]:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        instance: Reminder,
        persist_recipients: bool = True,
    ) -> Reminder:
        raise NotImplementedError

    @abstractmethod
    def persist_recipient(
        self,
        reminder_id: ReminderId,
        instance: ReminderRecipient,
    ) -> ReminderRecipient:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance_id: ReminderId):
        raise NotImplementedError

    @abstractmethod
    def delete_recipient(self, instance_id: ReminderRecipientId):
        raise NotImplementedError

    @abstractmethod
    def filter(self, tenant_id: TenantId) -> List[Reminder]:
        raise NotImplementedError


# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

from src.common.domain.enums.notifications import NotificationTemplateCategory
from src.common.domain.value_objects import TenantId
from src.notifications.domain.notification_template import NotificationTemplate


class NotificationTemplateRepository(ABC):
    @abstractmethod
    def find(
        self,
        tenant_id: TenantId,
        category: NotificationTemplateCategory,
    ) -> Optional[NotificationTemplate]:
        raise NotImplementedError

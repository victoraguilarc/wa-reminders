# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId
from src.notifications.application.responses import NotificationsResponse
from src.notifications.domain.repositories.notification import NotificationRepository


@dataclass
class PastNotificationsGetter(UseCase):
    tenant_id: TenantId
    notification_repository: NotificationRepository
    filter_last_days: Optional[int] = (None,)

    def execute(self) -> NotificationsResponse:
        notifications = self.notification_repository.filter(
            tenant_id=self.tenant_id,
            filter_last_days=self.filter_last_days,
        )
        return NotificationsResponse(notifications)

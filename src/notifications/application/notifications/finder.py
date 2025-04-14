# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import NotificationId, TenantId
from src.notifications.application.responses import NotificationResponse
from src.notifications.domain.exceptions import NotificationNotFound
from src.notifications.domain.repositories.notification import NotificationRepository


@dataclass
class NotificationFinder(UseCase):
    tenant_id: TenantId
    notification_id: NotificationId
    notification_repository: NotificationRepository

    def execute(self) -> ApiResponse:
        notification = self.notification_repository.find(
            tenant_id=self.tenant_id, notification_id=self.notification_id
        )
        if not notification:
            raise NotificationNotFound

        notification.recipients = self.notification_repository.get_recipients(
            tenant_id=self.tenant_id,
            notification_id=self.notification_id,
        )
        return NotificationResponse(notification)

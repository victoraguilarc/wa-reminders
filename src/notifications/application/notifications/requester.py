# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.value_objects import TenantId
from src.notifications.application.responses import NotificationResponse
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.domain.repositories.notification import NotificationRepository
from src.notifications.enums import NotificationStrategy


@dataclass
class NotificationRequester(ApiService):
    tenant_id: TenantId
    subject: str
    html_message: str
    targets: List[NotificationTarget]
    strategies: List[NotificationStrategy]
    notification_repository: NotificationRepository
    command_bus: CommandBus

    def execute(self) -> ApiResponse:
        notification = self.notification_repository.create(
            tenant_id=self.tenant_id,
            subject=self.subject,
            html_message=self.html_message,
            targets=self.targets,
            strategies=self.strategies,
        )
        # self.command_bus.dispatch(
        #     PerformNotificationCommand(
        #         tenant_id=self.tenant_id,
        #         notification_id=notification.id,
        #     )
        # )
        return NotificationResponse(notification)

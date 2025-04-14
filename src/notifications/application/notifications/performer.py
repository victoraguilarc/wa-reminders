# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from src.common.application.commands.notifications import SendEmailCommand
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.value_objects import NotificationId, TenantId
from src.notifications.application.notifications.recipients_getter import (
    NotificationRecipientsGetter,
)
from src.notifications.application.responses import NotificationResponse
from src.notifications.domain.exceptions import NotificationNotFound
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.domain.repositories.contact import NotificationRecipientRepository
from src.notifications.domain.repositories.notification import NotificationRepository
from src.notifications.enums import NotificationStatus, NotificationStrategy


@dataclass
class NotificationPerformer(ApiService):
    tenant_id: TenantId
    notification_id: NotificationId
    notification_repository: NotificationRepository
    notification_recipient_repository: NotificationRecipientRepository
    command_bus: CommandBus

    def execute(self) -> ApiResponse:
        notification = self.notification_repository.find(
            tenant_id=self.tenant_id,
            notification_id=self.notification_id,
        )

        if not notification:
            raise NotificationNotFound

        self._set_in_progress()
        notification.recipients = self._build_recipients(notification.targets)
        self._perform_strategies(notification)
        self._persist_updates(notification)

        return NotificationResponse(notification)

    def _set_in_progress(self):
        self.notification_repository.update(
            tenant_id=self.tenant_id,
            notification_id=self.notification_id,
            status=NotificationStatus.IN_PROGRESS,
        )

    def _build_recipients(self, targets: List[NotificationTarget]) -> List[NotificationRecipient]:
        return NotificationRecipientsGetter(
            tenant_id=self.tenant_id,
            targets=targets,
            notification_repository=self.notification_repository,
            notification_recipient_repository=self.notification_recipient_repository,
        ).execute()

    def _persist_updates(self, notification: Notification):
        self.notification_repository.attach_recipients(
            tenant_id=self.tenant_id,
            notification_id=self.notification_id,
            recipients=notification.recipients,
        )
        self.notification_repository.update(
            tenant_id=self.tenant_id,
            notification_id=self.notification_id,
            status=NotificationStatus.SENT,
        )

    def _perform_strategies(self, notification: Notification):
        for strategy in notification.strategies:
            if strategy == NotificationStrategy.EMAIL:
                self.command_bus.dispatch_batch(self._make_email_commands(notification))
            elif strategy == NotificationStrategy.SMS:
                pass
            elif strategy == NotificationStrategy.WHATSAPP:
                pass
            elif strategy == NotificationStrategy.PUSH_NOTIFICATION:
                pass

    @classmethod
    def _make_email_commands(cls, notification: Notification) -> List[SendEmailCommand]:
        commands = []
        for recipient in notification.recipients:
            commands.append(
                SendEmailCommand(
                    to_emails=[recipient.email],
                    template_name='retention/notification',
                    context={
                        'title': notification.subject,
                        'message': notification.message,
                        'html_message': notification.html_message,
                    },
                    subject=notification.subject,
                )
            )
        return commands

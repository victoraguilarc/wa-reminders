# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.value_objects import NotificationId, TenantId
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.enums import NotificationStatus, NotificationStrategy


class NotificationRepository(ABC):
    @abstractmethod
    def filter(
        self,
        tenant_id: TenantId,
        filter_last_days: Optional[int] = None,
    ) -> List[Notification]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
    ) -> Optional[Notification]:
        raise NotImplementedError

    @abstractmethod
    def get_recipients(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
    ) -> List[NotificationRecipient]:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        tenant_id: TenantId,
        subject: str,
        html_message: str,
        strategies: List[NotificationStrategy],
        targets: List[NotificationTarget],
        status: Optional[NotificationStatus] = None,
    ) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
        status: NotificationStatus = None,
        recipients_count: int = None,
    ) -> Optional[Notification]:
        raise NotImplementedError

    @abstractmethod
    def attach_recipients(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
        recipients: List[NotificationRecipient],
    ) -> Optional[Notification]:
        raise NotImplementedError

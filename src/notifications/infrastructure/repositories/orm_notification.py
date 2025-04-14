# -*- coding: utf-8 -*-

from datetime import timedelta
from typing import List, Optional

from django.db.models import Q
from django.utils.timezone import now

from src.common.database.models import NotificationORM, NotificationRecipientORM
from src.common.domain.value_objects import NotificationId, TenantId
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.domain.repositories.notification import NotificationRepository
from src.notifications.enums import NotificationStatus, NotificationStrategy
from src.notifications.infrastructure.builders.notification import NotificationBuilder
from src.notifications.infrastructure.builders.notification_recipient import (
    NotificationRecipientBuilder,
)
from src.notifications.utils import clean_html


class ORMNotificationRepository(NotificationRepository):
    def attach_recipients(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
        recipients: List[NotificationRecipient],
    ) -> Optional[Notification]:
        orm_instance = self._get_orm_instance(tenant_id, notification_id)
        if not orm_instance:
            return None
        for recipient in recipients:
            NotificationRecipientORM.objects.create(
                notification_id=notification_id,
                tenant_customer_id=recipient.id,
                delivered_at=now(),
            )

        orm_instance.recipients_count = len(recipients)
        orm_instance.save(update_fields=['recipients_count', 'updated_at'])

        return NotificationBuilder.build_from_orm(orm_instance)

    def update(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
        status: NotificationStatus = None,
        recipients_count: int = None,
    ) -> Optional[Notification]:
        orm_instance = self._get_orm_instance(tenant_id, notification_id)
        if not orm_instance:
            return None
        if status:
            orm_instance.new_status = status.value
        if recipients_count:
            orm_instance.recipients_count = recipients_count
        orm_instance.save()
        return NotificationBuilder.build_from_orm(orm_instance)

    def create(
        self,
        tenant_id: TenantId,
        subject: str,
        html_message: str,
        strategies: List[NotificationStrategy],
        targets: List[NotificationTarget],
        status: Optional[NotificationStatus] = None,
    ) -> Notification:
        status = status or NotificationStatus.PENDING.value
        raw_message = clean_html(html_message)
        orm_instance = NotificationORM.objects.create(
            subject=subject,
            html_message=html_message,
            message=raw_message,
            strategies=[str(strategy) for strategy in strategies],
            status=status,
            targets=[target.to_dict for target in targets],
            tenant_id=tenant_id,
        )
        return NotificationBuilder.build_from_orm(orm_instance)

    def filter(
        self,
        tenant_id: TenantId,
        filter_last_days: Optional[int] = None,
    ) -> List[Notification]:
        filter_criteria = Q(tenant_id=tenant_id)
        if filter_last_days:
            created_at_filter = now() - timedelta(days=filter_last_days)
            filter_criteria &= Q(created_at__gte=created_at_filter)
        orm_instances = NotificationORM.objects.filter(filter_criteria).order_by('-created_at')
        return [NotificationBuilder.build_from_orm(orm_instance) for orm_instance in orm_instances]

    def find(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
    ) -> Optional[Notification]:
        orm_instance = self._get_orm_instance(tenant_id, notification_id)
        if orm_instance:
            return NotificationBuilder.build_from_orm(orm_instance)
        return None

    def get_recipients(
        self,
        tenant_id: TenantId,
        notification_id: NotificationId,
    ) -> List[NotificationRecipient]:
        orm_instances = NotificationRecipientORM.objects.select_related('tenant_customer').filter(
            notification__tenant_id=tenant_id,
            notification_id=notification_id,
        )
        return [
            NotificationRecipientBuilder.from_recipient(orm_instance)
            for orm_instance in orm_instances
        ]

    @classmethod
    def _get_orm_instance(
        cls,
        tenant_id: TenantId,
        notification_id: NotificationId,
    ):
        return NotificationORM.objects.filter(
            tenant_id=tenant_id,
            uuid=notification_id,
        ).first()

# -*- coding: utf-8 -*-

from typing import Optional

from src.common.database.models import NotificationTemplateORM
from src.common.domain.enums.notifications import NotificationTemplateCategory
from src.common.domain.value_objects import TenantId
from src.notifications.domain.notification_template import NotificationTemplate
from src.notifications.domain.repositories.notification_template import (
    NotificationTemplateRepository,
)
from src.notifications.infrastructure.builders.notification_template import (
    NotificationTemplateBuilder,
)


class ORMNotificationTemplateRepository(NotificationTemplateRepository):
    def find(
        self,
        tenant_id: TenantId,
        category: NotificationTemplateCategory,
    ) -> Optional[NotificationTemplate]:
        orm_instance = NotificationTemplateORM.objects.filter(
            tenant_id=tenant_id,
            category=str(category),
        ).first()
        if not orm_instance:
            return None
        return NotificationTemplateBuilder.build_from_orm(orm_instance)

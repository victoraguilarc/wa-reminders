# -*- coding: utf-8 -*-

from src.common.database.models import NotificationTemplateORM
from src.common.domain.enums.notifications import NotificationTemplateCategory
from src.common.domain.value_objects import NotificationTemplateId
from src.notifications.domain.notification_template import NotificationTemplate


class NotificationTemplateBuilder(object):
    @classmethod
    def build_from_orm(cls, orm_instance: NotificationTemplateORM) -> NotificationTemplate:
        return NotificationTemplate(
            id=NotificationTemplateId(orm_instance.uuid),
            html_content=orm_instance.html_content,
            category=NotificationTemplateCategory.from_value(orm_instance.category),
            is_active=orm_instance.is_active,
            created_at=orm_instance.created_at,
        )

# -*- coding: utf-8 -*-

from src.common.database.models import NotificationORM
from src.common.domain.value_objects import NotificationId
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.enums import NotificationStatus, NotificationStrategy


class NotificationBuilder(object):
    @classmethod
    def build_from_orm(cls, orm_instance: NotificationORM) -> Notification:
        return Notification(
            id=NotificationId(orm_instance.uuid),
            subject=orm_instance.subject,
            message=orm_instance.message,
            html_message=orm_instance.html_message,
            status=NotificationStatus.from_value(orm_instance.status),
            strategies=[
                NotificationStrategy.from_value(strategy) for strategy in orm_instance.strategies
            ],
            targets=NotificationTarget.from_list(orm_instance.targets),
            recipients_count=orm_instance.recipients_count,
            created_at=orm_instance.created_at,
        )

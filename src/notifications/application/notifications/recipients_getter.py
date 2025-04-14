# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantClassId, TenantCustomerId, TenantId
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.domain.repositories.contact import NotificationRecipientRepository
from src.notifications.domain.repositories.notification import NotificationRepository
from src.notifications.enums import NotificationTargetType


@dataclass
class NotificationRecipientsGetter(UseCase):
    tenant_id: TenantId
    targets: List[NotificationTarget]
    notification_repository: NotificationRepository
    notification_recipient_repository: NotificationRecipientRepository

    def execute(self, *args, **kwargs) -> List[NotificationRecipient]:
        classes_ids = []
        tenant_customer_ids = []
        for target in self.targets:
            if target.type == NotificationTargetType.CLASS:
                classes_ids.append(TenantClassId(target.id))
            elif target.type == NotificationTargetType.CLASS_STUDENT:
                tenant_customer_ids.append(TenantCustomerId(target.id))
        class_recipients = self.notification_recipient_repository.get_from_classes_students(
            tenant_id=self.tenant_id,
            classes_ids=classes_ids,
        )
        single_recipients = self.notification_recipient_repository.get_from_tenant_customer_ids(
            tenant_id=self.tenant_id,
            tenant_customer_ids=tenant_customer_ids,
        )
        return class_recipients + single_recipients

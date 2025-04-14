from typing import List

from src.common.database.models import TenantCustomerORM
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.repositories.contact import NotificationRecipientRepository
from src.notifications.infrastructure.builders.notification_recipient import (
    NotificationRecipientBuilder,
)


class ORMNotificationRecipientRepository(NotificationRecipientRepository):
    def get_from_tenant_customer_ids(
        self,
        tenant_id: TenantId,
        tenant_customer_ids: List[TenantCustomerId],
    ) -> List[NotificationRecipient]:
        orm_instances = TenantCustomerORM.objects.select_related(
            'user',
            'phone_number',
        ).filter(
            uuid__in=tenant_customer_ids,
            tenant_id=tenant_id,
        )
        return [
            NotificationRecipientBuilder.from_tenant_customer(tenant_customer)
            for tenant_customer in orm_instances
        ]

    @classmethod
    def _get_class_student_related(cls):
        return (
            'tenant_class',
            'payment_plan',
            'tenant_customer',
            'tenant_customer__user',
            'tenant_customer__phone_number',
        )

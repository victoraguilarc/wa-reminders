from abc import ABC
from typing import List

from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.notifications.domain.notification_recipient import NotificationRecipient


class NotificationRecipientRepository(ABC):
    def get_from_tenant_customer_ids(
        self,
        tenant_id: TenantId,
        tenant_customer_ids: List[TenantCustomerId],
    ) -> List[NotificationRecipient]:
        raise NotImplementedError

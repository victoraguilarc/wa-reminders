from typing import Optional

from src.common.domain.context.client import ConsumerClient
from src.common.domain.enums.users import TenantCustomerCreationSource


def get_customer_creation_source(
    client: Optional[ConsumerClient],
) -> TenantCustomerCreationSource:
    if not client:
        return TenantCustomerCreationSource.UNDEFINED
    sources = {
        ConsumerClient.IOS: TenantCustomerCreationSource.MOBILE_ADMIN,
        ConsumerClient.ANDROID: TenantCustomerCreationSource.MOBILE_ADMIN,
        ConsumerClient.WEB: TenantCustomerCreationSource.TENANT_PAGE,
    }
    return sources.get(client.platform, TenantCustomerCreationSource.UNDEFINED)

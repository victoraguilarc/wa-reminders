from dataclasses import dataclass
from typing import Optional

from src.common.application.shortcuts.customers_site import get_members_callback_builder
from src.common.domain.exceptions.users import TenantCustomerNotFoundError
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerCallbackUrlMixin(object):
    tenant: Tenant
    tenant_customer_id: TenantCustomerId
    tenant_customer_repository: TenantCustomerRepository
    query_bus: QueryBus

    def get_tenant_customer(self) -> TenantCustomer:
        tenant_customer = self.tenant_customer_repository.find(
            tenant_id=self.tenant.id,
            tenant_customer_id=self.tenant_customer_id,
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError
        return tenant_customer

    def get_tenant_customers_callback_url(
        self,
        path: Optional[str] = None,
    ) -> Optional[CallbackBuilder]:
        return get_members_callback_builder(
            query_bus=self.query_bus,
            tenant_id=self.tenant.id,
            sub_path=path,
        )

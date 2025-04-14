from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.tenants import GetTenantByIdQuery, GetUserTenantContainerQuery
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.entities.user import User
from src.common.domain.value_objects import TenantId
from src.tenants.domain.exceptions import TenantNotFoundError


@dataclass
class GetTenantFromQueryMixin(object):
    tenant_id: TenantId
    query_bus: QueryBus

    def get_tenant(self) -> Optional[Tenant]:
        tenant: Optional[Tenant] = self.query_bus.ask(
            query=GetTenantByIdQuery(tenant_id=self.tenant_id),
        )
        if not tenant:
            raise TenantNotFoundError
        return tenant



@dataclass
class GetCurrentTenantMixin(object):
    query_bus: QueryBus

    def get_current_tenant(self, user: User) -> Optional[UserTenantContainer]:
        current_tenant: Optional[UserTenantContainer] = self.query_bus.ask(
            query=GetUserTenantContainerQuery(
                user_id=user.id,
                tenant_id=user.current_tenant_id,
            ),
        )
        return current_tenant

from typing import Optional

from src.common.application.queries.users import GetTenantUserByEmailQuery, GetTenantUserByIdQuery
from src.common.domain.exceptions.users import TenantUserNotFoundError
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import TenantUserId


class TenantUserActionView(object):
    bus_context = None
    tenant_context = None
    def _get_tenant_user(
        self,
        email: str,
    ) -> TenantUser:
        tenant_user: Optional[TenantUser] = self.bus_context.query_bus.ask(
            query=GetTenantUserByEmailQuery(
                tenant_id=self.tenant_context.tenant.id,
                email=email,
            ),
        )
        if not tenant_user:
            raise TenantUserNotFoundError
        return tenant_user


class TenantUserByIdActionView(object):
    bus_context = None
    tenant_context = None

    def _get_tenant_user(
        self,
        tenant_user_id: TenantUserId,
    ) -> TenantUser:
        tenant_user: Optional[TenantUser] = self.bus_context.query_bus.ask(
            query=GetTenantUserByIdQuery(
                tenant_id=self.tenant_context.tenant.id,
                tenant_user_id=tenant_user_id,
            ),
        )
        if not tenant_user:
            raise TenantUserNotFoundError
        return tenant_user

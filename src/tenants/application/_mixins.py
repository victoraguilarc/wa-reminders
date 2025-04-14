# -*- coding: utf-8 -*-
from typing import Optional

from src.common.application.queries.tenants import GetUserTenantContainerQuery
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_container import UserTenantContainer
from src.common.domain.value_objects import TenantId, UserId
from src.tenants.domain.exceptions import TenantNotFoundError
from src.tenants.domain.repositories.tenant import TenantRepository


class GetAccountTenantMixin(object):
    user_id: UserId
    tenant_id: TenantId
    tenant_repository: TenantRepository
    query_bus: QueryBus

    def get_user_tenant_container(self) -> Optional[UserTenantContainer]:
        return self.query_bus.ask(
            query=GetUserTenantContainerQuery(
                user_id=self.user_id,
                tenant_id=self.tenant_id,
            ),
        )


class GetTenantMixin(object):
    tenant_id: TenantId
    tenant_repository: TenantRepository

    def validate_tenant(self) -> Optional[Tenant]:
        tenant = self.tenant_repository.find(self.tenant_id)
        if not tenant:
            raise TenantNotFoundError
        return tenant

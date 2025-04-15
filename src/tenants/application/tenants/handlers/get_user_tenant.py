# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional

from src.common.application.queries.tenants import GetUserTenantContainerQuery, GetUserTenantsQuery
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.messaging.queries import QueryHandler
from src.tenants.application.tenants.use_cases.current_tenant_getter import (
    UserTenantContainerGetter,
)
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class GetUserTenantsHandler(QueryHandler):
    repository: TenantRepository

    def execute(self, query: GetUserTenantsQuery) -> List[Tenant]:
        return self.repository.get_user_tenants(query.user_id)


@dataclass
class GetUserTenantContainerHandler(QueryHandler):
    repository: TenantRepository

    def execute(
        self,
        query: GetUserTenantContainerQuery,
    ) -> Optional[UserTenantContainer]:
        return UserTenantContainerGetter(
            user_id=query.user_id,
            tenant_id=query.tenant_id,
            repository=self.repository,
        ).execute()

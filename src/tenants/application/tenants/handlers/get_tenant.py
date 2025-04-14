# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.tenants import GetTenantByIdQuery, GetTenantContainerByIdQuery
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_container import TenantContainer
from src.common.domain.messaging.queries import QueryHandler
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class GetTenantByIdHandler(QueryHandler):
    repository: TenantRepository

    def execute(self, query: GetTenantByIdQuery) -> Optional[Tenant]:
        return self.repository.find(query.tenant_id)


@dataclass
class GetTenantContainerByIdHandler(QueryHandler):
    repository: TenantRepository

    def execute(self, query: GetTenantContainerByIdQuery) -> Optional[TenantContainer]:
        return self.repository.find_container(query.tenant_id)

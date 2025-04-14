# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.common.application.queries.tenants import GetTenantResourcesByIdQuery
from src.common.domain.enums.tenants import LinkedSiteCategory
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant_container import TenantContainer
from src.common.domain.value_objects import TenantId
from src.tenants.domain.exceptions import TenantNotFoundError
from src.tenants.domain.repositories.tenant import TenantRepository
from src.tenants.domain.types.tenant_resources import TenantResources


@dataclass
class TenantFromSiteGetter(ApiService):
    domain: str
    category: LinkedSiteCategory
    tenant_repository: TenantRepository
    query_bus: QueryBus
    include_resources: bool = False

    def execute(self) -> Optional[TenantContainer]:
        tenant_container = self._get_tenant_container()

        if not tenant_container:
            logger.warning(f'TenantNotFound: {self.domain}')
            raise TenantNotFoundError

        if self.include_resources:
            tenant_container.tenant_resources = self._get_tenant_resources(
                tenant_id=tenant_container.tenant.id,
            )

        return tenant_container

    def _get_tenant_container(self):
        if self.category.is_members_site:
            return self.tenant_repository.get_tenant_from_members_site(
                domain=self.domain,
            )
        return None

    def _get_tenant_resources(
        self,
        tenant_id: TenantId,
    ) -> Optional[TenantResources]:
        return self.query_bus.ask(
            query=GetTenantResourcesByIdQuery(tenant_id=tenant_id),
        )


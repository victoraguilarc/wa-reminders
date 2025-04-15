from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.value_objects import TenantId, UserId
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class UserTenantContainerGetter(object):
    user_id: UserId
    repository: TenantRepository
    tenant_id: Optional[TenantId] = None

    def execute(self) -> Optional[UserTenantContainer]:
        tenant_container = (
            self.repository.find_container(self.tenant_id)
            if self.tenant_id
            else self.repository.get_user_tenant_container_fallback(self.user_id)
        )

        if not tenant_container:
            return None

        return UserTenantContainer(
            tenant=tenant_container.tenant,
            owner=tenant_container.owner,
        )

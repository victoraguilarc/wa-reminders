from dataclasses import dataclass
from typing import Optional

from src.common.domain.models.tenant_container import UserTenantContainer
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

        user_permissions = self.repository.get_user_permissions(
            user_id=self.user_id,
            tenant_id=tenant_container.tenant.id,
        )

        user_tenant_container = tenant_container.to_user_tenant_container
        user_tenant_container.permissions = user_permissions

        return user_tenant_container

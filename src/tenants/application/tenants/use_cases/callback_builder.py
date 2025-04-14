from dataclasses import dataclass
from typing import Optional

from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.infrastructure.callback_builder import QueryParamsCallbackBuilder
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class MembersSiteCallbackBuilder(UseCase):
    tenant_id: TenantId
    tenant_repository: TenantRepository
    fallback_hostname: str
    sub_path: Optional[str] = None

    def execute(self) -> CallbackBuilder:
        hostname = self._get_members_site_hostname(self.tenant_id)
        # Query params is used because Nextjs (the members site framework)
        # middleware does not have an easy way to handle paths
        return QueryParamsCallbackBuilder(
            hostname=f'{hostname}/{self.sub_path}' if self.sub_path else hostname,
        )

    def _get_members_site_hostname(
        self,
        tenant_id: TenantId,
    ) -> str:
        customers_site = self.tenant_repository.get_members_page(tenant_id)
        return customers_site.url if customers_site else self.fallback_hostname

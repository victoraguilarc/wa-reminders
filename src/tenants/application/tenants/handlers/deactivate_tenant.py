from dataclasses import dataclass

from src.common.application.commands.tenants import DeactivateTenantCommand
from src.common.application.helpers.strings import get_short_hash
from src.common.domain.enums.tenants import TenantStatus
from src.common.domain.messaging.commands import CommandHandler
from src.common.domain.entities.tenant import Tenant
from src.common.domain.value_objects import TenantSlug
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class DeactivateTenantCommandHandler(CommandHandler):
    repository: TenantRepository

    def execute(self, command: DeactivateTenantCommand):
        tenant = self.repository.find(tenant_id=command.tenant_id)

        if not self._is_tenant_deactivable(tenant):
            return

        tenant.slug = TenantSlug(f'{tenant.slug}-{get_short_hash(str(tenant.id))}')
        tenant.status = TenantStatus.INACTIVE
        tenant.owner = None

        self.repository.persist(tenant=tenant)

    def _is_tenant_deactivable(self, tenant: Tenant):
        return self.repository.get_owners_count(tenant.id) == 0

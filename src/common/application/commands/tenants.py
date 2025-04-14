from dataclasses import dataclass

from src.common.domain.messaging.commands import Command
from src.common.domain.value_objects import TenantId, UserId


@dataclass
class DeactivateTenantCommand(Command):
    tenant_id: TenantId
    owner_id: UserId

    @property
    def to_dict(self) -> dict:
        return {
            'tenant_id': str(self.tenant_id),
            'owner_id': str(self.owner_id),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'DeactivateTenantCommand':
        return cls(
            tenant_id=TenantId(kwargs['tenant_id']),
            owner_id=UserId(kwargs['owner_id']),
        )

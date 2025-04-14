from dataclasses import asdict, dataclass

from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.value_objects import TenantId


@dataclass
class TenantStats(AggregateRoot):
    tenant_id: TenantId
    customers_count: int
    users_count: int
    memberships_count: int

    @property
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'TenantStats':
        return cls(**kwargs)

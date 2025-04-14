from dataclasses import dataclass
from typing import List

from src.common.domain.enums.growth import TenantLeadChannel, TenantLeadStage
from src.common.domain.entities.list_filters import ListFilters


@dataclass
class TenantCustomerLeadsFilters(ListFilters):
    channels: List[TenantLeadChannel] = None
    statuses: List[TenantLeadStage] = None

    def __post_init__(self):
        self.statuses = self.statuses or []
        self.channels = self.channels or []

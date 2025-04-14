from dataclasses import dataclass
from typing import List

from src.common.domain.entities.list_filters import ListFilters
from src.common.domain.enums.users import TenantCustomerStatus


@dataclass
class TenantCustomersFilters(ListFilters):
    statuses: List[TenantCustomerStatus] = None

    def __post_init__(self):
        self.statuses = self.statuses or []

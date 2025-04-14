from dataclasses import dataclass
from typing import List

from src.common.domain.entities.list_filters import ListFilters
from src.common.domain.enums.users import TenantUserStatus


@dataclass
class TenantUsersFilters(ListFilters):
    statuses: List[TenantUserStatus] = None

    def __post_init__(self):
        self.statuses = self.statuses or []

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_container import UserTenantContainer
from src.common.domain.models.user_profile import UserProfile
from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class UserProfileContainer(AggregateRoot):
    user_profile: UserProfile
    current_tenant: UserTenantContainer
    tenants: List[Tenant] = None

    def __post_init__(self):
        self.tenants = self.tenants or []

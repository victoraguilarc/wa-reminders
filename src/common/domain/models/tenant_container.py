# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.user import User
from src.common.domain.types.permission import Permission


@dataclass
class TenantContainer(AggregateRoot):
    tenant: Tenant
    owner: User


@dataclass
class UserTenantContainer(TenantContainer):
    role: str = None
    permissions: List[Permission] = None

    def __post_init__(self):
        self.permissions = self.permissions or []
        self.role = self.role or 'ADMIN'


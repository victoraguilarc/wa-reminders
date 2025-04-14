# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.user import User
from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class TenantContainer(AggregateRoot):
    tenant: Tenant
    owner: User


@dataclass
class UserTenantContainer(TenantContainer):
    pass

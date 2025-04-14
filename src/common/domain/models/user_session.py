# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.models.tenant_container import UserTenantContainer
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import UserSessionToken


@dataclass
class TenantUserSession(AggregateRoot):
    profile: TenantUser
    current_tenant: UserTenantContainer
    token: Optional[UserSessionToken]


@dataclass
class TenantCustomerSession(AggregateRoot):
    profile: TenantCustomer
    token: UserSessionToken
    current_tenant: UserTenantContainer

# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.messaging.queries import Query
from src.common.domain.value_objects import TenantId, UserId


@dataclass
class GetTenantByIdQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantContainerByIdQuery(Query):
    tenant_id: TenantId


@dataclass
class GetQRCodeQuery(Query):
    content: str


@dataclass
class GetUserTenantsQuery(Query):
    user_id: UserId


@dataclass
class GetUserTenantContainerQuery(Query):
    user_id: UserId
    tenant_id: Optional[TenantId] = None


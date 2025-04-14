# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.messaging.queries import Query
from src.common.domain.value_objects import TenantClassId, TenantId, UserId, TenantPictureId


@dataclass
class GetTenantByIdQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantContainerByIdQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantMembersPageQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantTierQuery(Query):
    tenant_id: TenantId


@dataclass
class GetMembersSiteCallbackBuilderQuery(Query):
    tenant_id: TenantId
    sub_path: Optional[str] = None


@dataclass
class GetTenantByClassQuery(Query):
    tenant_class_id: TenantClassId


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


@dataclass
class GetTenantPictureByIdQuery(Query):
    tenant_id: TenantId
    instance_id: TenantPictureId


@dataclass
class GetTenantPictureByLabelQuery(Query):
    tenant_id: TenantId
    label: str


@dataclass
class GetTenantResourcesByIdQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantBranchesQuery(Query):
    tenant_id: TenantId


@dataclass
class GetTenantScheduleQuery(Query):
    tenant_id: TenantId

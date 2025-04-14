# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.messaging.queries import Query
from src.common.domain.value_objects import (
    TenantClassBatchId,
    TenantClassId,
    TenantClassScheduleId,
    TenantId,
    TenantSlug,
)


@dataclass
class GetTenantClassContainerBySlugsQuery(Query):
    tenant_slug: TenantSlug
    tenant_class_slug: str


@dataclass
class GetTenantClassByIdQuery(Query):
    tenant_id: TenantId
    tenant_class_id: TenantClassId
    exclude_soft_deleted: bool = False


@dataclass
class GetTenantClassScheduleByIdQuery(Query):
    tenant_id: TenantId
    tenant_class_id: TenantClassId
    tenant_class_schedule_id: TenantClassScheduleId


@dataclass
class GetTenantClassBatchByIdQuery(Query):
    tenant_id: TenantId
    tenant_class_batch_id: TenantClassBatchId


@dataclass
class GetTenantClassesQuery(Query):
    tenant_id: TenantId


@dataclass
class GetAgentTenantClassesQuery(Query):
    tenant_id: TenantId


@dataclass
class FilterSchedulesByTenantClassIdsQuery(Query):
    tenant_id: TenantId
    tenant_class_ids: List[TenantClassId]


@dataclass
class FilterTenanClassSchedulesByTenantIdQuery(Query):
    tenant_id: TenantId

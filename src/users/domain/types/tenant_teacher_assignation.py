# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.value_objects import TenantClassId, TenantCustomerId


@dataclass
class TeacherAssignationParams(AggregateRoot):
    tenant_customer_id: Optional[TenantCustomerId] = None
    tenant_class_id: Optional[TenantClassId] = None

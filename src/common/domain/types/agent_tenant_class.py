# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional

from src.common.domain.models.membership_plan import MembershipPlan
from src.common.domain.models.tenant_class import TenantClass
from src.common.domain.models.tenant_class_schedule import TenantClassSchedule
from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class AgentTenantClass(AggregateRoot):
    tenant_class: TenantClass
    schedules: List[TenantClassSchedule] = None
    membership_plans: List[MembershipPlan] = None

    def __post_init__(self):
        self.schedules = self.schedules or []
        self.membership_plans = self.membership_plans or []

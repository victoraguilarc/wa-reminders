# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class AgentTenantClassSession(AggregateRoot):
    meta_id: str
    class_name: str
    start_time: str
    finish_time: str
    free_spots: Optional[int] = None


@dataclass
class AgentTenantClassSessionGroup(AggregateRoot):
    day: date
    classes: List[AgentTenantClassSession]

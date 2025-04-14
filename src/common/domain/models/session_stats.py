# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class TenantClassSessionStats(object):
    students_count: int
    present_count: int
    absent_count: Optional[int] = None

    def __post_init__(self):
        self.absent_count = self.absent_count or self.students_count - self.present_count

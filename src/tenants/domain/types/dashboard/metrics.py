from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone


@dataclass
class DailyMetric(object):
    date: str
    attendees: int
    sales: float


@dataclass
class DailyMetricParams(object):
    range_dates: List[str]
    from_datetime: datetime
    to_datetime: datetime
    time_zone: TimeZone
    currency_code: CurrencyCode

# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

from pytz import utc

from src.common.domain.enums.locales import TimeZone


def now():
    """Returns timezoned now date."""
    return datetime.now(tz=utc)


def ago(**kwargs):
    """Returns timezoned minus a delta time."""
    return now() - timedelta(**kwargs)


def after(**kwargs):
    """Returns timezoned plus a delta time."""
    return now() + timedelta(**kwargs)


def generate_dates_range(start_date: date, end_date: date) -> list[str]:
    date_range = []

    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    # date_range.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)
    return date_range


def create_range_edges(
    start_date: date,
    end_date: date,
    time_zone: TimeZone = TimeZone.UTC,
) -> tuple[datetime, datetime]:
    _timezone = ZoneInfo(str(time_zone))

    start_datetime = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=_timezone,
    )

    end_datetime = datetime(
        year=end_date.year,
        month=end_date.month,
        day=end_date.day,
        hour=23,
        minute=59,
        second=59,
        microsecond=0,
        tzinfo=_timezone,
    )
    return start_datetime, end_datetime

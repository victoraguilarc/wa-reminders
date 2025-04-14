from datetime import datetime, timedelta

from src.common.constants import DEFAULT_PENDING_ACTION_EXPIRATION_IN_MINUTES
from src.common.helpers.time import TimeUtils


def get_action_valid_until() -> datetime:
    return (
        TimeUtils.utc_now()
        + timedelta(minutes=DEFAULT_PENDING_ACTION_EXPIRATION_IN_MINUTES)
    )


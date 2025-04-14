from dataclasses import dataclass

from src.common.domain.enums.memberships import MembershipStatus


@dataclass
class MembershipStat(object):
    status: MembershipStatus
    quantity: int
    change_rate: float

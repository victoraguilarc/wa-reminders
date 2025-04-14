from typing import Union

from src.common.database.models import (
    MembershipChangeORM,
    MembershipEventORM,
    MembershipPurchaseORM,
    MembershipRechargeORM,
)

MembershipEvents = Union[
    MembershipPurchaseORM, MembershipRechargeORM, MembershipChangeORM, MembershipEventORM
]

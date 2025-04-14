from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class TenantActivation(object):
    full_name: str
    email: Optional[str]
    phone_number: Optional[str]
    amount: Decimal
    activation_date: datetime

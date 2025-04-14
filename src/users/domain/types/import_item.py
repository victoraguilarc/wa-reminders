from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.common.domain.enums.users import TenantCustomerStatus


@dataclass
class TenantCustomerImportItem(object):
    alias: str
    first_name: str
    paternal_surname: str
    maternal_surname: Optional[str] = None
    status: TenantCustomerStatus = TenantCustomerStatus.ACTIVE
    email: Optional[str] = None
    dial_code: Optional[int] = None
    phone_number: Optional[str] = None
    created_at: Optional[datetime] = None
    plan_alias: Optional[str] = None
    num_passes: Optional[int] = None
    finishes_at: Optional[datetime] = None
    initial_amount: Optional[Decimal] = None

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from src.common.domain.models.membership import Membership
from src.common.domain.models.membership_plan import MembershipPlan
from src.common.domain.models.payment_method import PaymentMethod
from src.common.domain.models.payment_request import PaymentRequest
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.memberships import MembershipEventStatus
from src.common.domain.enums.payments import TimePeriod
from src.common.domain.value_objects import MembershipChangeId, TenantCustomerId, TenantId
from src.memberships.domain.entities.membership_change_params import MembershipChangeParams


@dataclass
class MembershipChange(object):
    id: MembershipChangeId
    tenant_id: TenantId
    status: MembershipEventStatus
    membership: Membership
    membership_plan: MembershipPlan
    tenant_customers: List[TenantCustomer]
    payment_method: Optional[PaymentMethod] = None
    payment_request: Optional[PaymentRequest] = None
    amount: Optional[Decimal] = None
    num_passes: Optional[int] = None
    num_periods: Optional[int] = None
    time_period: Optional[TimePeriod] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    @property
    def is_created(self):
        return self.status == MembershipEventStatus.CREATED

    @property
    def is_completed(self):
        return self.status == MembershipEventStatus.COMPLETED

    @property
    def is_pending_payment(self):
        return self.status == MembershipEventStatus.PENDING_PAYMENT

    @property
    def is_partially_paid(self):
        return self.status == MembershipEventStatus.PARTIALLY_PAID

    @property
    def is_cancelled(self):
        return self.status == MembershipEventStatus.CANCELLED

    @property
    def payment_qrcode_url(self):
        return self.payment_request.qrcode_url if self.payment_request else None

    @property
    def computed_amount(self) -> Decimal:
        return self.amount or self.membership_plan.amount

    @property
    def currency_code(self) -> CurrencyCode:
        return self.membership_plan.currency_code

    @property
    def has_initial_amount(self) -> bool:
        return self.amount is not None and self.amount > 0

    @property
    def tenant_customer_ids(self) -> List[TenantCustomerId]:
        return [tenant_customer.id for tenant_customer in self.tenant_customers]

    @property
    def has_changes(self):
        return (
            self.membership.membership_plan.id != self.membership_plan.id
            or self.amount is not None
            or self.num_passes is not None
            or self.num_periods is not None
            or self.time_period is not None
        )

    @property
    def is_free(self):
        return (
            self.membership_plan.is_free
            or self.payment_method is None
            or (self.amount is not None and self.amount == Decimal(0))
        )

    @property
    def is_manual(self):
        return self.payment_method is not None and self.payment_method.is_manual

    @property
    def is_online(self):
        return self.payment_method is not None and self.payment_method.is_online

    @property
    def to_persist_dict(self) -> dict:
        persist_dict = {
            'status': str(self.status),
            'membership_plan_id': str(self.membership_plan.id),
            'completed_at': self.completed_at,
            'cancelled_at': self.cancelled_at,
            'amount': self.amount,
            'num_passes': self.num_passes,
            'num_periods': self.num_periods,
            'time_period': (str(self.time_period) if self.time_period else None),
        }
        if self.payment_method:
            persist_dict['payment_method_id'] = str(self.payment_method.id)
        if self.payment_request:
            persist_dict['payment_request_id'] = str(self.payment_request.id)
        if self.membership:
            persist_dict['membership_id'] = str(self.membership.id)
        return persist_dict

    @property
    def channel_id(self):
        return f'MembershipChange@{self.id}'

    @property
    def concept(self) -> str:
        if len(self.tenant_customers) == 1:
            return self.tenant_customers[0].display_name
        elif len(self.tenant_customers) > 1:
            return f'{self.tenant_customers[0].display_name} +{len(self.tenant_customers) - 1}'
        return ''

    @property
    def to_tracking_dict(self):
        return {
            'id': str(self.id),
            'status': str(self.status),
        }

    def complete(self):
        self.status = MembershipEventStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    @classmethod
    def from_params(
        cls,
        params: MembershipChangeParams,
    ) -> 'MembershipChange':
        return cls(
            id=MembershipChangeId(uuid.uuid4()),
            tenant_id=params.tenant.id,
            membership=params.membership,
            status=MembershipEventStatus.PENDING_PAYMENT,
            membership_plan=params.membership_plan,
            payment_method=params.payment_method,
            tenant_customers=params.tenant_customers,
            amount=params.amount,
            num_passes=params.num_passes,
            num_periods=params.num_periods,
            time_period=params.time_period,
        )

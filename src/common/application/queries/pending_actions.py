from dataclasses import dataclass
from typing import Optional

from src.common.domain.messaging.queries import Query
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import RawPhoneNumber
from src.pending_actions.domain.callback_builder import CallbackBuilder


@dataclass
class GetEmailAddressVerificationQuery(Query):
    email: str
    callback_builder: CallbackBuilder
    from_email: Optional[str] = None
    send_async_email: bool = False


@dataclass
class GetPhoneNumberVerificationQuery(Query):
    raw_phone_number: RawPhoneNumber
    callback_builder: CallbackBuilder


@dataclass
class GetTenantCustomerSessionRedemptionQuery(Query):
    tenant_customer: TenantCustomer
    callback_builder: CallbackBuilder
    verify_phone_number: bool = False
    verify_email_address: bool = False


@dataclass
class GetTenantUserInvitationQuery(Query):
    tenant_user: TenantUser
    callback_builder: CallbackBuilder

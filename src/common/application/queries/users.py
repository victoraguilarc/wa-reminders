from dataclasses import dataclass
from typing import List, Optional

from src.common.domain.messaging.queries import Query
from src.common.domain.value_objects import RawPhoneNumber, TenantCustomerId, TenantId, TenantUserId, UserId


@dataclass
class GetTenantCustomerByEmailQuery(Query):
    tenant_id: TenantId
    email: str


@dataclass
class GetTenantCustomerByIdQuery(Query):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId


@dataclass
class GetTenantUserByIdQuery(Query):
    tenant_id: TenantId
    tenant_user_id: TenantUserId


@dataclass
class GetTenantUserByEmailQuery(Query):
    tenant_id: TenantId
    email: str


@dataclass
class GetTenantCustomerByAccessCodeQuery(Query):
    tenant_id: TenantId
    access_code: str


@dataclass
class GetTenantCustomerByParamsQuery(Query):
    tenant_id: TenantId
    tenant_customer_id: Optional[TenantCustomerId] = None
    email: Optional[str] = None
    phone_number: Optional[RawPhoneNumber] = None


@dataclass
class GetTenantCustomerForSessionQuery(Query):
    tenant_id: TenantId
    email: Optional[str] = None
    raw_phone_number: Optional[RawPhoneNumber] = None


@dataclass
class GetUserByEmailQuery(Query):
    email: str


@dataclass
class GetUserByIdQuery(Query):
    user_id: UserId


@dataclass
class GetTenantCustomersByIdsQuery(Query):
    tenant_id: TenantId
    tenant_customer_ids: List[TenantCustomerId]


@dataclass
class GetTenantCustomerByAliasQuery(Query):
    tenant_id: TenantId
    alias: str


@dataclass
class GetOrCreateEmailAddressQuery(Query):
    email: str


@dataclass
class GetOrCreatePhoneNumberQuery(Query):
    raw_phone_number: RawPhoneNumber

from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.value_objects import TenantCustomerId, TenantId


@dataclass
class TenantCustomerSessionRedemption(object):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    unverified_email_address: Optional[EmailAddress] = None
    unverified_phone_number: Optional[PhoneNumber] = None

    @property
    def to_dict(self):
        return {
            'tenant_id': str(self.tenant_id),
            'tenant_customer_id': str(self.tenant_customer_id),
            'unverified_email_address': (
                self.unverified_email_address.to_dict
                if self.unverified_email_address else None
            ),
            'unverified_phone_number': (
                self.unverified_phone_number.to_dict
                if self.unverified_phone_number else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            tenant_id=TenantId(data.get('tenant_id')),
            tenant_customer_id=TenantCustomerId(data.get('tenant_customer_id')),
            unverified_email_address=(
                EmailAddress.from_dict(data.get('unverified_email_address'))
                if data.get('unverified_email_address') else None
            ),
            unverified_phone_number=(
                PhoneNumber.from_dict(data.get('unverified_phone_number'))
                if data.get('unverified_phone_number') else None
            ),
        )

    @property
    def is_valid(self):
        return bool(self.tenant_id and self.tenant_customer_id)

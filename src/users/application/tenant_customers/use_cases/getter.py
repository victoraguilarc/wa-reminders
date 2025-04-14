from dataclasses import dataclass

from src.common.domain.exceptions.users import TenantCustomerNotFoundError
from src.common.domain.value_objects import RawPhoneNumber, TenantId
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerGetter(object):
    tenant_id: TenantId
    tenant_customer_repository: TenantCustomerRepository

    def get_by_email(self, email: str):
        tenant_customer = self.tenant_customer_repository.find_by_email(
            tenant_id=self.tenant_id,
            email=email,
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError
        return tenant_customer

    def get_by_phone_number(self, phone_number: RawPhoneNumber):
        tenant_customer = self.tenant_customer_repository.find_by_phone_number(
            tenant_id=self.tenant_id,
            phone_number=phone_number,
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError
        return tenant_customer

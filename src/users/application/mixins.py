# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from src.common.application.shortcuts.simple_buidlers.raw_phone_number import RawPhoneNumberBuilder
from src.common.domain.exceptions.common import EmailIsAlreadyUsedError
from src.common.domain.exceptions.users import TenantCustomerNotFoundError
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.domain.exceptions import PhoneNumberIsAlreadyUsedError
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class GetTenantCustomerMixin(object):
    repository: TenantCustomerRepository

    def get_tenant_customer(
        self,
        tenant_id: TenantId,
        tenant_customer_id: TenantCustomerId,
    ) -> Optional[TenantCustomer]:
        tenant_customer = self.repository.find(
            tenant_id=tenant_id,
            tenant_customer_id=tenant_customer_id,
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError
        return tenant_customer

    def _check_email_and_phone_uniqueness(
        self,
        tenant_customer: TenantCustomer,
        excluded_ids: List[TenantCustomerId] = None,
    ):
        if tenant_customer.email_address and not self.repository.is_email_available(
            tenant_id=tenant_customer.tenant_id,
            email=tenant_customer.email_address.email,
            excluded_ids=excluded_ids,
        ):
            raise EmailIsAlreadyUsedError

        if tenant_customer.phone_number and not self.repository.is_phone_number_available(
            tenant_id=tenant_customer.tenant_id,
            dial_code=tenant_customer.phone_number.dial_code,
            phone_number=tenant_customer.phone_number.phone_number,
            excluded_ids=excluded_ids,
        ):
            raise PhoneNumberIsAlreadyUsedError

    @classmethod
    def _prefix_phone_number(cls, tenant_customer: TenantCustomer):
        if not tenant_customer.phone_number:
            return
        raw_phone_number = RawPhoneNumberBuilder.build(
            dial_code=tenant_customer.phone_number.dial_code,
            phone_number=tenant_customer.phone_number.phone_number,
        )
        tenant_customer.phone_number.load_raw_phone_number(raw_phone_number)

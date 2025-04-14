# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.application.mixins import GetTenantCustomerMixin
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class TenantCustomerDetailer(GetTenantCustomerMixin, ApiService):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    repository: TenantCustomerRepository

    def execute(self, *args, **kwargs) -> TenantCustomer:
        return self.get_tenant_customer(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
        )

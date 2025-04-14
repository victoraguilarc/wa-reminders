# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.responses.tenant_customer import TenantCustomerResponse
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.application.mixins import GetTenantCustomerMixin
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class TenantCustomerDeleter(GetTenantCustomerMixin, ApiService):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    repository: TenantCustomerRepository

    def execute(self, *args, **kwargs) -> ApiResponse:
        self.get_tenant_customer(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
        )
        self.repository.delete(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
        )
        # TODO Publish stream_events
        return TenantCustomerResponse()

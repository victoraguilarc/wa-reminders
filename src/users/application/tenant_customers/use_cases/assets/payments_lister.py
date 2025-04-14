# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.models.list_filters import ListFilters
from src.common.domain.models.pagination import Page
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerPaymentsGetter(ApiService):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    list_filters: ListFilters
    repository: TenantCustomerRepository

    def execute(self, *args, **kwargs) -> Page:
        return self.repository.get_payments_paginated(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
            list_filters=self.list_filters,
        )

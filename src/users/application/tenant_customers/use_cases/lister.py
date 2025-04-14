# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.entities.pagination import Page
from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId
from src.users.domain.filters.tenant_customers import TenantCustomersFilters
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class TenantCustomersLister(UseCase):
    tenant_id: TenantId
    repository: TenantCustomerRepository
    list_filters: TenantCustomersFilters

    def execute(self, *args, **kwargs) -> Page:
        return self.repository.filter_paginated(
            tenant_id=self.tenant_id,
            list_filters=self.list_filters,
        )

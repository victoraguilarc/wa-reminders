# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.entities.pagination import Page
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantId
from src.users.domain.filters.tenant_users import TenantUsersFilters
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUsersLister(ApiService):
    tenant_id: TenantId
    repository: TenantUserRepository
    list_filters: TenantUsersFilters

    def execute(self, *args, **kwargs) -> Page:
        return self.repository.filter_paginated(
            tenant_id=self.tenant_id,
            list_filters=self.list_filters,
        )

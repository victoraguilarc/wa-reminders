from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.entities.list_filters import ListFilters
from src.common.domain.entities.pagination import Page
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId, TenantSlug, UserId


class TenantRepository(ABC):
    @abstractmethod
    def find(self, tenant_id: TenantId) -> Optional[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def find_by_slug(self, slug: TenantSlug) -> Optional[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def find_by_wa_session(self, session_name: str) -> Optional[TenantWhatsappSession]:
        raise NotImplementedError

    @abstractmethod
    def get_tenants_counter(self, user_id: UserId) -> int:
        raise NotImplementedError

    @abstractmethod
    def persist(self, tenant: Tenant) -> Tenant:
        raise NotImplementedError


    @abstractmethod
    def find_by_id(self, tenant_id: TenantId) -> Optional[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def get_active_tenants(self) -> List[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def get_user_tenants(self, user_id: UserId) -> List[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def get_user_tenants_paginated(
        self,
        user_id: UserId,
        list_filters: ListFilters,
    ) -> Page:
        raise NotImplementedError

    @abstractmethod
    def switch_tenant(self, user_id: UserId, tenant_id: TenantId):
        raise NotImplementedError


    @abstractmethod
    def get_owners_count(self, tenant_id: TenantId) -> int:
        raise NotImplementedError

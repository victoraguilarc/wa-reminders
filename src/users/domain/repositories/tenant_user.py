# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.models.pagination import Page
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.models.user_context import UserContext
from src.common.domain.value_objects import RawPhoneNumber, TenantId, TenantUserId, UserId
from src.users.domain.filters.tenant_users import TenantUsersFilters


class TenantUserRepository(ABC):
    @abstractmethod
    def filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantUsersFilters,
    ) -> List[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def filter_paginated(
        self,
        tenant_id: TenantId,
        list_filters: TenantUsersFilters,
    ) -> Page:
        raise NotImplementedError

    @abstractmethod
    def filter_by_ids(
        self,
        tenant_id: TenantId,
        tenant_users_ids: List[TenantUserId],
    ) -> List[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def filter_by_tenant(
        self,
        tenant_id: TenantId,
    ) -> List[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def is_email_available(
        self,
        tenant_id: TenantId,
        email: str,
        excluded_ids: List[TenantUserId] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_phone_number_available(
        self,
        tenant_id: TenantId,
        dial_code: int,
        phone_number: str,
        excluded_ids: List[TenantUserId] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(
        self,
        tenant_id: TenantId,
        email: str,
    ) -> Optional[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def find_by_phone_number(
        self,
        tenant_id: TenantId,
        phone_number: RawPhoneNumber,
    ) -> Optional[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
    ) -> Optional[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def find_user_context(
        self,
        user_id: UserId,
        tenant_id: TenantId,
    ) -> Optional[UserContext]:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        instance: TenantUser,
    ) -> TenantUser:
        raise NotImplementedError

    @abstractmethod
    def check_password(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
        current_password: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_password(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
        new_password: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def create_from_user(
        self,
        tenant_id: TenantId,
        user_id: UserId,
        status: TenantUserStatus,
        is_owner: bool,
    ) -> TenantUser:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
    ):
        raise NotImplementedError

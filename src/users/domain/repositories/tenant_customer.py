# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.enums.users import TenantCustomerStatus, TenantCustomerCreationSource
from src.common.domain.models.pagination import Page
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.user import SimplePerson
from src.common.domain.models.user_context import UserContext
from src.common.domain.value_objects import (
    RawPhoneNumber,
    TenantCustomerId,
    TenantId,
    UserId,
)
from src.users.domain.filters.tenant_customers import TenantCustomersFilters


class TenantCustomerRepository(ABC):
    @abstractmethod
    def filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomersFilters,
    ) -> List[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def filter_paginated(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomersFilters,
    ) -> Page:
        raise NotImplementedError

    @abstractmethod
    def filter_by_ids(
        self,
        tenant_id: TenantId,
        tenant_customer_ids: List[TenantCustomerId],
    ) -> List[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def filter_by_tenant(
        self,
        tenant_id: TenantId,
    ) -> List[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def is_email_available(
        self,
        tenant_id: TenantId,
        email: str,
        excluded_ids: List[TenantCustomerId] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_phone_number_available(
        self,
        tenant_id: TenantId,
        dial_code: int,
        phone_number: str,
        excluded_ids: List[TenantCustomerId] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(
        self,
        tenant_id: TenantId,
        email: str,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_by_phone_number(
        self,
        tenant_id: TenantId,
        phone_number: RawPhoneNumber,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_by_alias(
        self,
        tenant_id: TenantId,
        alias: str,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        tenant_id: TenantId,
        tenant_customer_id: TenantCustomerId,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_by_params(
        self,
        tenant_id: TenantId,
        tenant_customer_id: Optional[TenantCustomerId] = None,
        email: Optional[str] = None,
        phone_number: Optional[RawPhoneNumber] = None,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_for_session(
        self,
        tenant_id: TenantId,
        email: Optional[str] = None,
        raw_phone_number: Optional[RawPhoneNumber] = None,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_by_access_code(
        self,
        tenant_id: TenantId,
        access_code: str,
    ) -> Optional[TenantCustomer]:
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
        instance: TenantCustomer,
    ) -> TenantCustomer:
        raise NotImplementedError

    @abstractmethod
    def get_or_create_from_person(
        self,
        tenant_id: TenantId,
        person: SimplePerson,
        tenant_customer_id: Optional[TenantCustomerId] = None,
        status: Optional[TenantCustomerStatus] = None,
        creation_source: Optional[TenantCustomerCreationSource] = None,
    ) -> TenantCustomer:
        raise NotImplementedError

    @abstractmethod
    def create_from_user(
        self,
        tenant_id: TenantId,
        user_id: UserId,
        status: TenantCustomerStatus,
    ) -> TenantCustomer:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        tenant_id: TenantId,
        tenant_customer_id: TenantCustomerId,
    ):
        raise NotImplementedError

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.entities.user_profile import UserProfile
from src.common.domain.value_objects import EmailAddressId, PhoneNumberId, TenantId, UserId


class SessionRepository(ABC):
    @abstractmethod
    def find_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_tenant_user(
        self,
        user_id: UserId,
        tenant_id: TenantId,
    ) -> Optional[TenantUser]:
        raise NotImplementedError

    @abstractmethod
    def find_tenant_customer(
        self,
        user_id: UserId,
        tenant_id: TenantId,
    ) -> Optional[TenantCustomer]:
        raise NotImplementedError

    @abstractmethod
    def find_context_by_email(
        self,
        email: str,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[UserProfile]:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_context(
        self,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[UserContext]:
        raise NotImplementedError

    @abstractmethod
    def find_email_address(
        self,
        email_address_id: EmailAddressId,
    ) -> Optional[EmailAddress]:
        raise NotImplementedError

    @abstractmethod
    def find_phone_number(
        self,
        phone_number_id: PhoneNumberId,
    ) -> Optional[PhoneNumber]:
        raise NotImplementedError

    @abstractmethod
    def has_valid_password(
        self,
        user: User,
        password: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_session_tenants(
        self,
        user: User,
    ) -> List[Tenant]:
        raise NotImplementedError

    @abstractmethod
    def estimate_current_tenant(
        self,
        user: User,
    ) -> Optional[Tenant]:
        raise NotImplementedError

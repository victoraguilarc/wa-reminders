# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from src.common.application.queries.tenants import GetUserTenantContainerQuery, GetUserTenantsQuery
from src.common.application.shortcuts.simple_buidlers.raw_phone_number import RawPhoneNumberBuilder
from src.common.domain.exceptions.common import EmailIsAlreadyUsedError
from src.common.domain.exceptions.users import UserNotFoundError, TenantUserNotFoundError
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.value_objects import TenantId, TenantUserId, UserId
from src.users.domain.exceptions import PhoneNumberIsAlreadyUsedError, TenantUserMustHaveAtLeastOneAuthMethodError
from src.users.domain.repositories.tenant_user import TenantUserRepository
from src.users.domain.repositories.user import UserRepository


@dataclass
class GetTenantUserContextMixin(object):
    user_id: UserId
    user_repository: UserRepository
    tenant_user_repository: TenantUserRepository
    query_bus: QueryBus
    path_hostname: str
    tenant_id: Optional[TenantId]

    def get_user_context(self) -> Optional[UserContext]:
        if self.tenant_id:
            user = self.tenant_user_repository.find_user_context(
                user_id=self.user_id,
                tenant_id=self.tenant_id,
            )
        else:
            user = self.user_repository.find_user_context(user_id=self.user_id)
        if not user:
            raise UserNotFoundError
        return user

    def get_current_user_tenant_container(self, user: User) -> Optional[UserTenantContainer]:
        user_tenant_container: Optional[UserTenantContainer] = self.query_bus.ask(
            query=GetUserTenantContainerQuery(
                user_id=user.id,
                tenant_id=user.current_tenant_id,
            ),
        )
        return user_tenant_container

    def get_tenants(self) -> List[Tenant]:
        user_tenants: Optional[List[Tenant]] = self.query_bus.ask(
            query=GetUserTenantsQuery(user_id=self.user_id)
        )
        return user_tenants


@dataclass
class GetTenantUserMixin(object):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    repository: TenantUserRepository

    def get_tenant_user(self) -> TenantUser:
        tenant_user = self.repository.find(
            tenant_id=self.tenant_id,
            tenant_user_id=self.tenant_user_id,
        )
        if not tenant_user:
            raise TenantUserNotFoundError
        return tenant_user


@dataclass
class TenantUserValidationsMixin(object):
    repository: TenantUserRepository

    def _check_email_and_phone_uniqueness(
        self,
        tenant_user: TenantUser,
        excluded_ids: List[TenantUserId] = None,
    ):
        user = tenant_user.user
        has_email_address = user and user.email_address
        has_phone_number = user and user.phone_number
        if (
            has_email_address
            and not self.repository.is_email_available(
                tenant_id=tenant_user.tenant_id,
                email=user.email_address.email,
                excluded_ids=excluded_ids,
            )
        ):
            raise EmailIsAlreadyUsedError

        if (
            has_phone_number
            and not self.repository.is_phone_number_available(
                tenant_id=tenant_user.tenant_id,
                dial_code=user.phone_number.dial_code,
                phone_number=user.phone_number.phone_number,
                excluded_ids=excluded_ids,
            )
        ):
            raise PhoneNumberIsAlreadyUsedError

    @classmethod
    def _prefix_phone_number(cls, tenant_user: TenantUser):
        if not tenant_user.user.phone_number:
            return
        raw_phone_number = RawPhoneNumberBuilder.build(
            dial_code=tenant_user.user.phone_number.dial_code,
            phone_number=tenant_user.user.phone_number.phone_number,
        )
        tenant_user.user.phone_number.load_raw_phone_number(raw_phone_number)

    @classmethod
    def _check_auth_methods(cls, tenant_user: TenantUser):
        has_any_auth_method = tenant_user.email_address or tenant_user.phone_number
        if not has_any_auth_method:
            raise TenantUserMustHaveAtLeastOneAuthMethodError

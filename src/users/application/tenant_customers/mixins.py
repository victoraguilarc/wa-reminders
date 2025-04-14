# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from src.common.application.queries.tenants import GetUserTenantContainerQuery, GetUserTenantsQuery
from src.common.domain.exceptions.users import UserNotFoundError
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.value_objects import TenantId, UserId
from src.users.domain.repositories import TenantCustomerRepository
from src.users.domain.repositories.user import UserRepository


@dataclass
class GetTenantCustomerMixin(object):
    tenant_id: TenantId
    user_id: UserId
    user_repository: UserRepository
    tenant_customer_repository: TenantCustomerRepository
    query_bus: QueryBus

    def get_user_context(self) -> Optional[UserContext]:
        if self.tenant_id:
            user = self.tenant_customer_repository.find_user_context(
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

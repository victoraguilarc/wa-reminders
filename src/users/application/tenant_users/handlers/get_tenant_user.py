from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import (
    GetTenantUserByIdQuery, GetTenantUserByEmailQuery,
)
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.entities.tenant_user import TenantUser
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class GetTenantUserByIdHandler(QueryHandler):
    repository: TenantUserRepository

    def execute(
        self,
        query: GetTenantUserByIdQuery,
    ) -> Optional[TenantUser]:
        return self.repository.find(
            tenant_id=query.tenant_id,
            tenant_user_id=query.tenant_user_id,
        )


@dataclass
class GetTenantUserByEmailHandler(QueryHandler):
    repository: TenantUserRepository

    def execute(
        self,
        query: GetTenantUserByEmailQuery,
    ) -> Optional[TenantUser]:
        return self.repository.find_by_email(
            tenant_id=query.tenant_id,
            email=query.email,
        )




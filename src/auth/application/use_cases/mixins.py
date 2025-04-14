from dataclasses import dataclass
from typing import Optional

from src.auth.domain.exceptions import InvalidCredentialsForTenant
from src.auth.domain.repositories import SessionRepository
from src.common.domain.models.tenant_container import UserTenantContainer
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.models.user import User


@dataclass
class GetAuthTenantUserMixin(object):
    session_repository: SessionRepository

    def get_tenant_user(
        self,
        user: User,
        current_tenant: Optional[UserTenantContainer] = None,
    ) -> TenantUser:
        if  not current_tenant:
            return TenantUser.empty(user)

        tenant_user = self.session_repository.find_tenant_user(
            user_id=user.id,
            tenant_id=current_tenant.tenant.id,
        )

        if not tenant_user:
            raise InvalidCredentialsForTenant

        return tenant_user

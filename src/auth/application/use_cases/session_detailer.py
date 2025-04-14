# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.auth.application.use_cases.mixins import GetAuthTenantUserMixin
from src.auth.domain.repositories import SessionRepository
from src.common.application.mixins.tenant import GetCurrentTenantMixin
from src.common.domain.exceptions.users import UserNotFoundError
from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.tenant_container import UserTenantContainer
from src.common.domain.entities.user import User
from src.common.domain.entities.user_session import TenantUserSession
from src.common.domain.value_objects import UserId
from src.users.domain.repositories.user import UserRepository


@dataclass
class UserSessionDetailer(GetAuthTenantUserMixin, GetCurrentTenantMixin, UseCase):
    user_id: UserId
    user_repository: UserRepository
    session_repository: SessionRepository

    def execute(self, *args, **kwargs) -> TenantUserSession:
        user = self._get_user()
        current_tenant: Optional[UserTenantContainer] = self.get_current_tenant(user)

        tenant_user = self.get_tenant_user(user, current_tenant)

        return TenantUserSession(
            profile=tenant_user,
            current_tenant=self.get_current_tenant(tenant_user.user),
            token=None,
        )

    def _get_user(self) -> Optional[User]:
        user = self.user_repository.find(user_id=self.user_id)
        if not user:
            raise UserNotFoundError
        return user

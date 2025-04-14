# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.auth.application.use_cases.mixins import GetAuthTenantUserMixin
from src.auth.domain.exceptions import InvalidCredentials
from src.auth.domain.repositories.session import SessionRepository
from src.common.application.mixins.tenant import GetCurrentTenantMixin
from src.common.application.queries.auth import GetUserSessionTokenQuery
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant_container import UserTenantContainer
from src.common.domain.models.user import User
from src.common.domain.models.user_session import TenantUserSession
from src.common.domain.value_objects import UserSessionToken


@dataclass
class LoginSessionBuilder(GetCurrentTenantMixin, GetAuthTenantUserMixin, UseCase):
    email: str
    password: str
    session_repository: SessionRepository
    query_bus: QueryBus
    path_hostname: str

    def execute(self, *args, **kwargs) -> TenantUserSession:
        user = self._fin_user_by_email()
        current_tenant: Optional[UserTenantContainer] = self.get_current_tenant(user)
        tenant_user = self.get_tenant_user(user, current_tenant)

        has_valid_password = self.session_repository.has_valid_password(
            user=user,
            password=self.password,
        )

        if not has_valid_password:
            raise InvalidCredentials

        return TenantUserSession(
            profile=tenant_user,
            token=self._get_user_session_token(user),
            current_tenant=self.get_current_tenant(user),
        )

    def _fin_user_by_email(self) -> User:
        user = self.session_repository.find_by_email(self.email)
        if not user:
            raise InvalidCredentials
        return user


    def _get_user_session_token(self, user: User) -> Optional[UserSessionToken]:
        return self.query_bus.ask(
            query=GetUserSessionTokenQuery(user=user),
        )

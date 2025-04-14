# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.exceptions.users import InvalidPasswordError, SamePasswordsError
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantId, TenantUserId
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserPasswordUpdater(ApiService):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    repository: TenantUserRepository
    current_password: str
    new_password: str

    def execute(self) -> TaskResultStatus:
        if self.current_password == self.new_password:
            raise SamePasswordsError

        is_current_password_valid = self.repository.check_password(
            tenant_id=self.tenant_id,
            tenant_user_id=self.tenant_user_id,
            current_password=self.current_password,
        )
        if not is_current_password_valid:
            raise InvalidPasswordError

        self.repository.update_password(
            tenant_id=self.tenant_id,
            tenant_user_id=self.tenant_user_id,
            new_password=self.new_password,
        )

        return (
            TaskResultStatus.SUCCESS
            if is_current_password_valid
            else TaskResultStatus.FAILURE
        )

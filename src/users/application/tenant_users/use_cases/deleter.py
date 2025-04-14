# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantId, TenantUserId
from src.users.application.tenant_users.mixins import GetTenantUserMixin
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserDeleter(GetTenantUserMixin, ApiService):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    repository: TenantUserRepository

    def execute(self):
        self.get_tenant_user()
        self.repository.delete(self.tenant_id, self.tenant_user_id)

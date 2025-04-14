# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.interfaces.services import ApiService
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.application.tenant_users.mixins import GetTenantUserMixin
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserDetailer(GetTenantUserMixin, ApiService):
    tenant_id: TenantId
    tenant_user_id: TenantCustomerId
    repository: TenantUserRepository

    def execute(self, *args, **kwargs) -> TenantUser:
        return self.get_tenant_user()

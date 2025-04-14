# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional

from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import TenantId, TenantUserId, TenantRoleId
from src.users.application.tenant_users.mixins import GetTenantUserMixin, TenantUserValidationsMixin
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserUpdater(GetTenantUserMixin, TenantUserValidationsMixin, ApiService):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    repository: TenantUserRepository
    updated_instance: TenantUser
    updated_fields: List[str]
    query_bus: QueryBus
    tenant_role_id: Optional[TenantRoleId] = None

    def execute(self, *args, **kwargs) -> TenantUser:
        tenant_user = self.get_tenant_user()
        tenant_user.overload(
            new_instance=self.updated_instance,
            properties=self.updated_fields,
        )
        self._prefix_phone_number(tenant_user)
        self._check_email_and_phone_uniqueness(
            tenant_user=tenant_user,
            excluded_ids=[self.tenant_user_id],
        )
        return self.repository.persist(tenant_user)

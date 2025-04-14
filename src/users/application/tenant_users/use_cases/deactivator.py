# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.commands.tenants import DeactivateTenantCommand
from src.common.application.commands.users import DeactivateUserCommand
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.value_objects import TenantId, TenantUserId
from src.users.application.tenant_users.mixins import GetTenantUserMixin
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserProfileDeleter(GetTenantUserMixin, ApiService):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    repository: TenantUserRepository
    command_bus: CommandBus

    def execute(self):
        tenant_user = self.get_tenant_user()
        self.command_bus.dispatch(
            command=DeactivateUserCommand(tenant_user.user.id),
        )
        self.repository.delete(
            tenant_id=self.tenant_id,
            tenant_user_id=self.tenant_user_id,
        )
        self.command_bus.dispatch(
            command=DeactivateTenantCommand(
                tenant_id=self.tenant_id,
                owner_id=tenant_user.user.id,
            ),
        )

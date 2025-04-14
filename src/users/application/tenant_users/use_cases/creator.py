# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.commands.pending_actions import RequestTenantUserInvitationCommand
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.users.application.tenant_users.mixins import TenantUserValidationsMixin
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class TenantUserCreator(TenantUserValidationsMixin, UseCase):
    repository: TenantUserRepository
    new_instance: TenantUser
    command_bus: CommandBus
    query_bus: QueryBus
    send_async_invitation: bool = False
    send_invitation: bool = False

    def execute(self) -> TenantUser:
        self._check_auth_methods(self.new_instance)
        self._prefix_phone_number(self.new_instance)
        self._check_email_and_phone_uniqueness(
            tenant_user=self.new_instance,
        )
        tenant_user = self.repository.persist(self.new_instance)
        self._process_invitation(tenant_user)
        return tenant_user

    def _process_invitation(self, tenant_user: TenantUser):
        if not self.send_invitation:
            return
        self.command_bus.dispatch(
            command=RequestTenantUserInvitationCommand(
                tenant_id=tenant_user.tenant_id,
                tenant_user_id=tenant_user.id,
            ),
            run_async=self.send_async_invitation,
        )

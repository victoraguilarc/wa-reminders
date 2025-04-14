from dataclasses import dataclass

from src.common.application.commands.users import (
    CreateBasicTenantCustomerCommand,
    RegisterCustomerInTenantCommand,
)
from src.common.domain.messaging.commands import CommandBus, CommandHandler
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class CreateBasicTenantCustomerHandler(CommandHandler):
    repository: TenantCustomerRepository
    command_bus: CommandBus

    def execute(
        self,
        command: CreateBasicTenantCustomerCommand,
    ):
        tenant_customer = self.repository.get_or_create_from_person(
            tenant_id=command.tenant_id,
            person=command.person,
            status=command.status,
            creation_source=command.creation_source,
        )


@dataclass
class RegisterCustomerInTenantHandler(CommandHandler):
    repository: TenantCustomerRepository
    command_bus: CommandBus

    def execute(self, command: RegisterCustomerInTenantCommand):
        tenant_customer = self.repository.create_from_user(
            tenant_id=command.tenant_id,
            user_id=command.user.id,
            status=command.status,
        )


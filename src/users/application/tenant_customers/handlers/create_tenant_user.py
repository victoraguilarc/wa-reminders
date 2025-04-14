from dataclasses import dataclass

from src.common.application.commands.users import RegisterUserInTenantCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class RegisterUserInTenantHandler(CommandHandler):
    repository: TenantUserRepository

    def execute(self, command: RegisterUserInTenantCommand):
        self.repository.create_from_user(
            tenant_id=command.tenant_id,
            user_id=command.user.id,
            status=command.status,
            is_owner=command.is_owner,
        )

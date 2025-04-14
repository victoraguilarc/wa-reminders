from dataclasses import dataclass

from src.common.application.commands.users import PersistTenantUserCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories.tenant_user import TenantUserRepository


@dataclass
class PersistTenantUserHandler(CommandHandler):
    repository: TenantUserRepository

    def execute(self, command: PersistTenantUserCommand):
        self.repository.persist(command.instance)

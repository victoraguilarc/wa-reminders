from dataclasses import dataclass

from src.common.application.commands.users import PersistTenantCustomerCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class PersistTenantCustomerHandler(CommandHandler):
    repository: TenantCustomerRepository

    def execute(self, command: PersistTenantCustomerCommand):
        self.repository.persist(command.instance)

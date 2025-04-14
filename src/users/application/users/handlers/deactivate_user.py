from dataclasses import dataclass

from src.common.application.commands.users import DeactivateUserCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories.user import UserRepository


@dataclass
class DeactivateUserHandler(CommandHandler):
    repository: UserRepository

    def execute(self, command: DeactivateUserCommand):
        self.repository.delete(user_id=command.user_id)

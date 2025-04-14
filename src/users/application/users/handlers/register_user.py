from dataclasses import dataclass

from src.common.application.commands.users import RegisterUserCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.application.users.user_cases.setter import UserSetter
from src.users.domain.repositories.user import UserRepository


@dataclass
class RegisterUserHandler(CommandHandler):
    repository: UserRepository

    def execute(self, command: RegisterUserCommand):
        UserSetter(
            instance=command.instance,
            raw_password=command.raw_password,
            repository=self.repository,
        ).execute()

from dataclasses import dataclass

from src.common.application.commands.users import SetUserPasswordCommand
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories.user import UserRepository


@dataclass
class SetUserPasswordHandler(CommandHandler):
    repository: UserRepository

    def execute(self, command: SetUserPasswordCommand):
        self.repository.set_password(
            user_id=command.user_id,
            new_password=command.new_password,
        )

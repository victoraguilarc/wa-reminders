from dataclasses import dataclass

from src.common.application.commands.notifications import SendEmailCommand
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.entities.user import User


@dataclass
class UserResetPasswordNotifier(UseCase):
    user: User
    command_bus: CommandBus
    callback_url: str
    extra_context: dict = None

    def execute(self):
        extra_context = self.extra_context or {}
        self.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[self.user.email],
                context={
                    **extra_context,
                    'action_link': self.callback_url,
                },
                template_name='actions/user/reset_password',
            ),
        )

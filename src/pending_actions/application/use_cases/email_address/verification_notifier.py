from dataclasses import dataclass

from src.common.application.commands.notifications import SendEmailCommand
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus


@dataclass
class EmailAddressVerificationNotifier(UseCase):
    email: str
    command_bus: CommandBus
    callback_url: str
    send_async_email: bool = False

    def execute(self):
        self.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[self.email],
                context={
                    'action_link': self.callback_url,
                },
                template_name='actions/email_address/verification',
            ),
            run_async=self.send_async_email,
        )

from dataclasses import dataclass

from src.common.application.commands.notifications import SendEmailCommand
from src.common.domain.messaging.commands import CommandHandler
from src.notifications.domain.interfaces.email_sender import EmailSender


@dataclass
class SendEmailHandler(CommandHandler):
    email_sender: EmailSender
    default_from_email: str

    def execute(self, command: SendEmailCommand):
        self.email_sender.send_email(
            subject=command.subject,
            from_email=command.from_email or self.default_from_email,
            to_emails=command.to_emails,
            context=command.context,
            template_name=command.template_name,
        )

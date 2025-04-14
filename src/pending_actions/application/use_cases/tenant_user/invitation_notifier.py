from dataclasses import dataclass

from src.common.application.commands.notifications import SendEmailCommand
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.entities.tenant_user import TenantUser


@dataclass
class TenantUserInvitationNotifier(UseCase):
    tenant_user: TenantUser
    command_bus: CommandBus
    callback_url: str

    def execute(self):
        self.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[self.tenant_user.email],
                context={
                    'first_name': self.tenant_user.first_name,
                    'action_link': self.callback_url,
                },
                template_name='actions/tenant_user/invitation',
            ),
        )

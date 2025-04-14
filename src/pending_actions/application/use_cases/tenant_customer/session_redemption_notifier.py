from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.notifications import SendEmailCommand, SendWhatsappSequenceCommand
from src.common.application.queries.pending_actions import GetTenantCustomerSessionRedemptionQuery
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.whatsapp_message import (
    TemplateWhatsappMessage,
    TextWhatsappMessage,
)
from src.pending_actions.domain.callback_builder import CallbackBuilder


@dataclass
class TenantCustomerSessionRedemptionNotifier(UseCase):
    tenant: Tenant
    tenant_customer: TenantCustomer
    command_bus: CommandBus
    query_bus: QueryBus
    callback_builder: CallbackBuilder
    send_async: bool = False

    def execute(self):
        self._send_email_notification()
        self._send_whatsapp_notification()

    def _send_email_notification(self):
        session_redemption: Optional[PendingActionContext] = self.query_bus.ask(
            query=GetTenantCustomerSessionRedemptionQuery(
                tenant_customer=self.tenant_customer,
                callback_builder=self.callback_builder,
                verify_email_address=True,
            ),
        )
        self.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[self.tenant_customer.email],
                context={
                    'tenant_name': self.tenant.name,
                    'first_name': self.tenant_customer.first_name,
                    'action_link': session_redemption.callback_url,
                    'access_code': self.tenant_customer.access_code_url,
                },
                template_name='actions/tenant_customer/session_redemption',
            ),
        )

    def _send_whatsapp_notification(self):
        session_redemption: Optional[PendingActionContext] = self.query_bus.ask(
            query=GetTenantCustomerSessionRedemptionQuery(
                tenant_customer=self.tenant_customer,
                callback_builder=self.callback_builder,
                verify_phone_number=True,
            ),
        )
        self.command_bus.dispatch(
            command=SendWhatsappSequenceCommand(
                tenant_id=self.tenant.id,
                phone_number=self.tenant_customer.international_number,
                messages=[
                    TemplateWhatsappMessage(
                        template_name='actions/tenant_customer/session_redemption',
                        context={
                            'tenant_name': self.tenant.name,
                            'first_name': self.tenant_customer.first_name,
                        },
                    ),
                    TextWhatsappMessage(content=session_redemption.callback_url),
                ],
            ),
        )


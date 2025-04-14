from dataclasses import dataclass

from src.common.application.commands.notifications import (
    SendWhatsappCommand,
    SendWhatsappSequenceCommand,
)
from src.common.domain.messaging.commands import CommandHandler
from src.common.domain.messaging.queries import QueryBus
from src.notifications.application.whatsap_session.name_getter import WhatsappSessionNameGetter
from src.notifications.domain.interfaces.whatsapp_sender import WhatsappSender


@dataclass
class SendWhatsappHandler(CommandHandler):
    whatsapp_sender: WhatsappSender
    query_bus: QueryBus

    def execute(self, command: SendWhatsappCommand):
        session_name = WhatsappSessionNameGetter(
            tenant_id=command.tenant_id,
            query_bus=self.query_bus,
        ).execute()

        self.whatsapp_sender.send_message(
            session_name=session_name,
            phone_number=command.phone_number,
            message=command.message,
        )


@dataclass
class SendWhatsappSequenceHandler(CommandHandler):
    whatsapp_sender: WhatsappSender
    query_bus: QueryBus

    def execute(self, command: SendWhatsappSequenceCommand):
        session_name = WhatsappSessionNameGetter(
            tenant_id=command.tenant_id,
            query_bus=self.query_bus,
        ).execute()

        for message in command.messages:
            self.whatsapp_sender.send_message(
                session_name=session_name,
                phone_number=command.phone_number,
                message=message,
            )

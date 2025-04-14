# -*- coding: utf-8 -*-

from django.conf import settings

from src.common.application.commands.notifications import (
    PublishStreamEventCommand,
    SendEmailCommand,
    SendWhatsappCommand,
    SendWhatsappSequenceCommand,
)
from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.application.messaging.handlers import SendEmailHandler
from src.notifications.application.messaging.handlers.publish_stream_event import (
    PublishStreamEventHandler,
)
from src.notifications.application.messaging.handlers.send_whatsapp import (
    SendWhatsappHandler,
    SendWhatsappSequenceHandler,
)


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    bus.command_bus.subscribe(
        command=SendEmailCommand,
        handler=SendEmailHandler(
            email_sender=domain_context.email_sender,
            default_from_email=settings.DEFAULT_FROM_EMAIL,
        ),
    )
    bus.command_bus.subscribe(
        command=SendWhatsappCommand,
        handler=SendWhatsappHandler(
            query_bus=bus.query_bus,
            whatsapp_sender=domain_context.whatsapp_sender,
        ),
    )
    bus.command_bus.subscribe(
        command=SendWhatsappSequenceCommand,
        handler=SendWhatsappSequenceHandler(
            query_bus=bus.query_bus,
            whatsapp_sender=domain_context.whatsapp_sender,
        ),
    )
    bus.command_bus.subscribe(
        command=PublishStreamEventCommand,
        handler=PublishStreamEventHandler(
            event_publisher=domain_context.stream_events_publisher,
        ),
    )

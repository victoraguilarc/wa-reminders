from django.conf import settings

from src.common.domain.entities.wa_session import (
    WhatsappSessionWebhook,
    WhatsappSessionWebhookEvent,
    WhatsappSessionWebhookHeader,
)


def get_whatsapp_webhooks():
    return [
        # WhatsappSessionWebhook(
        #     url=settings.WHATSAPP_API_AGENTS_WEBHOOK,
        #     events=[
        #         WhatsappSessionWebhookEvent.MESSAGE,
        #         WhatsappSessionWebhookEvent.SESSION_STATUS,
        #     ],
        # ),
        WhatsappSessionWebhook(
            url=settings.WHATSAPP_API_SESSION_WEBHOOK,
            events=[
                WhatsappSessionWebhookEvent.SESSION_STATUS,
            ],
            custom_headers=[
                WhatsappSessionWebhookHeader(
                    name='X-Api-Key',
                    value=settings.WHATSAPP_API_SESSION_API_KEY,
                ),
            ],
        ),
    ]


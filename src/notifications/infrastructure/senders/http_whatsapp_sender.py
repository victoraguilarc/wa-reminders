from dataclasses import dataclass
from typing import Optional

import requests
from django.template.loader import render_to_string
from django.utils import translation

from src.common.domain.interfaces.whatsapp import WhatsappMessage
from src.common.domain.models.whatsapp_message import (
    ImageWhatsappMessage,
    TemplateWhatsappMessage,
    TextWhatsappMessage,
)
from src.notifications.domain.interfaces.whatsapp_sender import WhatsappSender


@dataclass
class HttpWhatsappSender(WhatsappSender):
    api_hostanme: str
    api_key: str

    def send_message(
        self,
        session_name: str,
        phone_number: str,
        message: WhatsappMessage,
    ):
        if isinstance(message, TemplateWhatsappMessage):
            self._send_template_message(
                session_name=session_name,
                phone_number=phone_number,
                message=message,
            )
        elif isinstance(message, TextWhatsappMessage):
            self._send_text_message(
                session_name=session_name,
                phone_number=phone_number,
                message=message,
            )
        elif isinstance(message, ImageWhatsappMessage):
            self._send_image_message(
                session_name=session_name,
                phone_number=phone_number,
                message=message,
            )
        else:
            raise NotImplementedError

    def _send_template_message(
        self,
        session_name: str,
        phone_number: str,
        message: TemplateWhatsappMessage,
    ):
        with translation.override(message.language.value):
            template_path = f'whatsapp/{message.template_name}.txt'
            text_body: str = render_to_string(
                template_name=template_path,
                context=message.context,
            )
            response = requests.post(
                url=f'{self.api_hostanme}/api/sendText',
                headers=self._get_headers(),
                json=self._build_message_body(
                    session_name=session_name,
                    phone_number=phone_number,
                    message=text_body,
                ),
            )
            response.raise_for_status()

    def _send_text_message(
        self,
        session_name: str,
        phone_number: str,
        message: TextWhatsappMessage,
    ):
        response = requests.post(
            url=f'{self.api_hostanme}/api/sendText',
            headers=self._get_headers(),
            json=self._build_message_body(
                session_name=session_name,
                phone_number=phone_number,
                message=message.content,
            ),
        )
        response.raise_for_status()

    def _send_image_message(
        self,
        session_name: str,
        phone_number: str,
        message: ImageWhatsappMessage,
    ):
        with translation.override(message.language.value):
            caption_text = self._build_caption_text(message)

            payload = {
                'chatId': f'{phone_number}@s.whatsapp.net',
                'session': session_name,
                'file': {
                    'url': message.image_url
                },
            }
            if caption_text:
                payload['caption'] = caption_text

            response = requests.post(
                url=f'{self.api_hostanme}/api/sendImage',
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()

    def _get_headers(self) -> dict:
        return {
            'accept': 'application/json',
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json',
        }

    @classmethod
    def _build_caption_text(cls, message: ImageWhatsappMessage) -> Optional[str]:
        template_path = f'whatsapp/{message.caption_template}.txt'
        if message.caption_template and message.caption_context:
            caption_text: str = render_to_string(
                template_name=template_path,
                context=message.caption_context,
            )
            return caption_text.strip()
        return None

    @classmethod
    def _build_message_body(
        cls,
        session_name: str,
        phone_number: str,
        message: str,
    ) -> dict:
        return {
            'chatId': f'{phone_number}@s.whatsapp.net',
            'text': message.strip(),
            'session': session_name,
        }

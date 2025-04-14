# -*- coding: utf-8 -*-

from dataclasses import asdict, dataclass
from typing import List, Optional

from src.common.domain.interfaces.whatsapp import WhatsappMessage
from src.common.domain.messaging.commands import Command
from src.common.domain.entities.stream_event import StreamEvent
from src.common.domain.value_objects import TenantId


@dataclass
class SendEmailCommand(Command):
    to_emails: List[str]
    template_name: str
    context: dict
    subject: Optional[str] = None
    from_email: Optional[str] = None

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendEmailCommand':
        return cls(**kwargs)


@dataclass
class SendWhatsappCommand(Command):
    phone_number: str
    message: WhatsappMessage
    tenant_id: Optional[TenantId] = None

    @property
    def to_dict(self) -> dict:
        return {
            'phone_number': self.phone_number,
            'message': self.message.to_dict,
            'tenant_id': (
                str(self.tenant_id)
                if self.tenant_id is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendWhatsappCommand':
        return cls(
            phone_number=kwargs['phone_number'],
            message=WhatsappMessage.from_dict(kwargs['message']),
            tenant_id=(
                TenantId(kwargs['tenant_id'])
                if kwargs.get('tenant_id') is not None
                else None
            ),
        )


@dataclass
class SendWhatsappSequenceCommand(Command):
    phone_number: str
    messages: List[WhatsappMessage]
    tenant_id: Optional[TenantId] = None

    @property
    def to_dict(self) -> dict:
        return {
            'phone_number': self.phone_number,
            'messages': [message.to_dict for message in self.messages],
            'tenant_id': (
                str(self.tenant_id)
                if self.tenant_id is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendWhatsappSequenceCommand':
        return cls(
            phone_number=kwargs['phone_number'],
            messages=[
                WhatsappMessage.from_dict(message)
                for message in kwargs['messages']
            ],
            tenant_id=(
                TenantId(kwargs['tenant_id'])
                if kwargs.get('tenant_id') is not None
                else None
            ),
        )


@dataclass
class PublishStreamEventCommand(Command):
    channel_id: str
    stream_event: StreamEvent

    @property
    def to_dict(self) -> dict:
        return {
            'channel_id': self.channel_id,
            'stream_event': self.stream_event.to_dict,
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PublishStreamEventCommand':
        return cls(
            channel_id=kwargs['channel_id'],
            stream_event=StreamEvent.from_dict(kwargs['stream_event']),
        )

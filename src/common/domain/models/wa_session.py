from dataclasses import dataclass
from typing import Optional, List

from src.common.domain import BaseEnum
from src.common.domain.enums.tenants import WhatsappSessionStatus


@dataclass
class WhatsappAccount(object):
    id: str
    push_name: str

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'pushName': self.push_name,
        }


@dataclass
class WhatsappSessionQRCode(object):
    session_name: str
    format: str
    value: str


@dataclass
class WhatsappSession(object):
    session_name: str
    status: WhatsappSessionStatus
    config: dict
    me: Optional[WhatsappAccount] = None

    @property
    def phone_number(self) -> Optional[str]:
        if self.me:
            return self.me.id.split('@c.us')[0]
        return None

    @property
    def to_dict(self) -> dict:
        return {
            'sessionName': self.session_name,
            'status': self.status.value,
            'config': self.config,
            'me': self.me.to_dict if self.me else None,
        }

    @property
    def is_linked(self) -> bool:
        return bool(self.me)

@dataclass
class WhatsappSessionWebhookHeader(object):
    name: str
    value: str

    @property
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
        }


class WhatsappSessionWebhookEvent(BaseEnum):
    MESSAGE = 'message'
    SESSION_STATUS = 'session.status'


@dataclass
class WhatsappSessionWebhook(object):
    url: str
    events: List[WhatsappSessionWebhookEvent]
    custom_headers: List[WhatsappSessionWebhookHeader] = None

    @property
    def to_dict(self) -> dict:
        custom_headers = self.custom_headers or []
        return {
            'url': self.url,
            'events': [event.value for event in self.events],
            'customHeaders': [header.to_dict for header in custom_headers],
        }


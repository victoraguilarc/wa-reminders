# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.presenters.tenant import TenantPresenter
from src.common.domain.context.locale import LocaleContext
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.entities.wa_session import WhatsappSessionQRCode


@dataclass
class TenantWhatsappSessionPresenter(object):
    instance: TenantWhatsappSession
    locale_context: LocaleContext

    @property
    def to_dict(self) -> dict:
        return {
            'id': str(self.instance.id),
            'session_name': self.instance.session_name,
            'status': str(self.instance.status),
            'phone_number': self.instance.phone_number,
            'messaging_enabled': self.instance.messaging_enabled,
            'agents_enabled': self.instance.agents_enabled,
        }

@dataclass()
class TenantWhatsappSessionQRCodePresenter(object):
    instance: WhatsappSessionQRCode
    locale_context: LocaleContext

    @property
    def to_dict(self) -> dict:
        return{
            'session_name': self.instance.session_name,
            'format': self.instance.format,
            'value': self.instance.value,
        }


@dataclass
class AgentTenantWhatsappSessionPresenter(object):
    instance: TenantWhatsappSession
    locale_context: LocaleContext

    @property
    def to_dict(self) -> dict:
        return {
            'tenant': TenantPresenter(self.instance.tenant, self.locale_context).to_dict,
            'session': TenantWhatsappSessionPresenter(self.instance, self.locale_context).to_dict,
        }

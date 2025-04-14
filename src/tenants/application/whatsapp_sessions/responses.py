# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from src.common.constants import INSTANCE_DELETED_RESPONSE
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.entities.wa_session import WhatsappSessionQRCode
from src.tenants.application.whatsapp_sessions.presenters import (
    TenantWhatsappSessionPresenter,
    AgentTenantWhatsappSessionPresenter, TenantWhatsappSessionQRCodePresenter,
)


@dataclass
class AgentTenantWhatsappSessionResponse(ApiResponse):
    instance: Optional[TenantWhatsappSession] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:

        if not self.instance:
            return INSTANCE_DELETED_RESPONSE

        return AgentTenantWhatsappSessionPresenter(self.instance, locale_context).to_dict


@dataclass
class TenantWhatsappSessionResponse(ApiResponse):
    instance: Optional[TenantWhatsappSession] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:

        if not self.instance:
            return INSTANCE_DELETED_RESPONSE

        return TenantWhatsappSessionPresenter(self.instance, locale_context).to_dict


@dataclass
class TenantWhatsappSessionQRCodeResponse(ApiResponse):
    instance: Optional[WhatsappSessionQRCode] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:

        if not self.instance:
            return INSTANCE_DELETED_RESPONSE

        return TenantWhatsappSessionQRCodePresenter(self.instance, locale_context).to_dict


@dataclass
class TenantWhatsappSessionsResponse(ApiResponse):
    instances: List[TenantWhatsappSession]

    def render(self, locale_context: LocaleContext) -> list:
        return [
            TenantWhatsappSessionPresenter(instance, locale_context).to_dict
            for instance in self.instances
        ]

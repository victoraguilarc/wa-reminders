# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.application.whatsapp_sessions.mixins import GetTenantWhatsappSessionMixin
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionDeleter(GetTenantWhatsappSessionMixin, UseCase):
    tenant_id: TenantId
    instance_id: TenantWhatsappSessionId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager

    def execute(self):
        instance = self.get_by_id(self.instance_id)
        self.repository.delete(
            tenant_id=self.tenant_id,
            instance_id=instance.id,
        )
        self.session_manager.delete_session(
            session_name=instance.session_name,
        )


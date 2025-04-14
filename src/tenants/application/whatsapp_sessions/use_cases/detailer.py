from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.application.whatsapp_sessions.mixins import (
    GetTenantWhatsappSessionMixin,
    RefreshTenantWhatsappSessionMixin,
)
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionDetailer(
    GetTenantWhatsappSessionMixin,
    RefreshTenantWhatsappSessionMixin,
    UseCase,
):
    tenant_id: TenantId
    instance_id: TenantWhatsappSessionId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager

    def execute(self) -> TenantWhatsappSession:
        local_session = self.get_by_id(self.instance_id)
        return self.refresh_instance(local_session)

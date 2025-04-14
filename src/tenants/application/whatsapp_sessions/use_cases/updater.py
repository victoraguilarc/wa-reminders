from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.entities.wa_session import WhatsappSession
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.application.whatsapp_sessions.mixins import GetTenantWhatsappSessionMixin
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionUpdater(GetTenantWhatsappSessionMixin, UseCase):
    tenant_id: TenantId
    instance_id: TenantWhatsappSessionId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager

    def execute(self) -> TenantWhatsappSession:
        local_session = self.get_by_id(self.instance_id)
        remote_session = self.session_manager.update_session(
            instance=WhatsappSession(
                session_name=local_session.session_name,
                status=local_session.status,
                config=local_session.config,
            ),
        )
        # TODO: probably we need to handle more properties override here
        local_session.status = remote_session.status
        self.repository.persist(tenant_id=self.tenant_id, instance=local_session)
        return local_session

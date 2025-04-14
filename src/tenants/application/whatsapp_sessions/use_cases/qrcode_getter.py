from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.wa_session import WhatsappSessionQRCode
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.application.whatsapp_sessions.mixins import GetTenantWhatsappSessionMixin
from src.tenants.domain.exceptions import TenantWhatsappUnavailableQRCodeError
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionQRCodeGetter(GetTenantWhatsappSessionMixin, UseCase):
    tenant_id: TenantId
    instance_id: TenantWhatsappSessionId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager

    def execute(self) -> WhatsappSessionQRCode:
        local_session = self.get_by_id(self.instance_id)
        remote_session = self.session_manager.get_session(local_session.session_name)

        if remote_session.status != local_session.status:
            local_session.status = remote_session.status

        if not local_session.is_scan_qr_code:
            raise TenantWhatsappUnavailableQRCodeError

        session_qrcode = self.session_manager.get_auth_qr(local_session.session_name)
        self.repository.persist(tenant_id=self.tenant_id, instance=local_session)

        return session_qrcode

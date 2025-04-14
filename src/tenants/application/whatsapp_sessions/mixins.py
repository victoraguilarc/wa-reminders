from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.domain.exceptions import TenantWhatsappSessionNotFoundError
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class GetTenantWhatsappSessionMixin(object):
    tenant_id: TenantId
    repository: TenantWhatsappSessionRepository

    def get_by_id(self, instance_id: TenantWhatsappSessionId) -> TenantWhatsappSession:
        instance: Optional[TenantWhatsappSession] = self.repository.find(
            tenant_id=self.tenant_id,
            instance_id=instance_id,
        )

        if not instance:
            raise TenantWhatsappSessionNotFoundError

        return instance

@dataclass
class GetTenantWhatsappSessionNameMixin(object):
    repository: TenantWhatsappSessionRepository

    def get_by_session_name(
        self,
        session_name: str,
        raise_exception: bool = True,
    ) -> TenantWhatsappSession:
        instance: Optional[TenantWhatsappSession] = self.repository.find_by_session_name(
            session_name=session_name,
        )
        if not instance and raise_exception:
            raise TenantWhatsappSessionNotFoundError
        return instance



@dataclass
class RefreshTenantWhatsappSessionMixin(object):
    tenant_id: TenantId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager

    def refresh_instance(
        self,
        instance: TenantWhatsappSession,
    ) -> Optional[TenantWhatsappSession]:
        remote_session = self.session_manager.get_session(instance.session_name)

        if not remote_session:
            return None

        # TODO: probably we need to handle more properties override here
        instance.status = remote_session.status
        if remote_session.me:
            instance.phone_number = remote_session.phone_number
        self.repository.persist(tenant_id=self.tenant_id, instance=instance)
        return instance

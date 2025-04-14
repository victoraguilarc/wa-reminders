from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.tenants.application.whatsapp_sessions.mixins import GetTenantWhatsappSessionMixin
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository


@dataclass
class TenantWhatsappSessionPatcher(GetTenantWhatsappSessionMixin, UseCase):
    tenant_id: TenantId
    instance_id: TenantWhatsappSessionId
    updated_properties: dict
    repository: TenantWhatsappSessionRepository

    def execute(self) -> TenantWhatsappSession:
        instance = self.get_by_id(self.instance_id)

        for key, value in self.updated_properties.items():
            setattr(instance, key, value)

        return self.repository.persist(
            tenant_id=self.tenant_id,
            instance=instance,
        )

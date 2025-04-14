from src.common.database.models.tenant_wa_session import TenantWhatsappSessionORM
from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantWhatsappSessionId
from src.common.infrastructure.builders.tenant import build_tenant


def build_tenant_whatsapp_session(
    orm_instance: TenantWhatsappSessionORM,
) -> TenantWhatsappSession:
    return TenantWhatsappSession(
        id=TenantWhatsappSessionId(orm_instance.uuid),
        tenant=build_tenant(orm_instance.tenant),
        session_name=orm_instance.session_name,
        status=WhatsappSessionStatus.from_value(orm_instance.status),
        phone_number=orm_instance.phone_number,
        messaging_enabled=orm_instance.messaging_enabled,
        agents_enabled=orm_instance.agents_enabled,
        config=orm_instance.config,
    )

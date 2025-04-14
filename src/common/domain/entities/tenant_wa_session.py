from dataclasses import dataclass
from typing import Optional

from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.entities.tenant import Tenant
from src.common.domain.value_objects import TenantWhatsappSessionId


@dataclass
class TenantWhatsappSession(AggregateRoot):
    id: TenantWhatsappSessionId
    tenant: Tenant
    session_name: str
    status: WhatsappSessionStatus
    phone_number: Optional[str] = None
    messaging_enabled: bool = True
    agents_enabled: bool = True
    config: dict = None


    @property
    def is_starting(self):
        return self.status == WhatsappSessionStatus.STARTING

    @property
    def is_stopped(self):
        return self.status == WhatsappSessionStatus.STOPPED

    @property
    def is_scan_qr_code(self):
        return self.status == WhatsappSessionStatus.SCAN_QR_CODE

    @property
    def is_failed(self):
        return self.status == WhatsappSessionStatus.FAILED

    @property
    def is_working(self):
        return self.status == WhatsappSessionStatus.WORKING

    def __post_init__(self):
        self.config = self.config or {}

    @property
    def to_persist_dict(self):
        return {
            'tenant_id': self.tenant.id,
            'status': str(self.status),
            'session_name': self.session_name,
            'phone_number': self.phone_number,
            'messaging_enabled': self.messaging_enabled,
            'agents_enabled': self.agents_enabled,
            'config': self.config,
        }

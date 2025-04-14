from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.notifications import GetTenantWhatsappSessionNameQuery
from src.common.constants import DEFAULT_WHATSAPP_API_SESSION
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus


@dataclass
class WhatsappSessionNameGetter(UseCase):
    query_bus: QueryBus
    tenant_id: Optional[str] = None

    def execute(self) -> str:
        if not self.tenant_id:
            return DEFAULT_WHATSAPP_API_SESSION

        session_name: Optional[str] = self.query_bus.ask(
            query=GetTenantWhatsappSessionNameQuery(self.tenant_id)
        )

        if not session_name:
            return DEFAULT_WHATSAPP_API_SESSION

        return session_name


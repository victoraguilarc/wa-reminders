from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.notifications import GetTenantWhatsappSessionNameQuery
from src.common.domain.messaging.queries import QueryHandler
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository


@dataclass
class GetTenantWhatsappSessionNameHandler(QueryHandler):
    repository: TenantWhatsappSessionRepository

    def execute(self, query: GetTenantWhatsappSessionNameQuery) -> Optional[str]:
        return self.repository.get_messaging_session_name(
            tenant_id=query.tenant_id,
        )

from dataclasses import dataclass

from src.common.domain.messaging.queries import Query
from src.common.domain.value_objects import TenantId


@dataclass
class GetTenantWhatsappSessionNameQuery(Query):
    tenant_id: TenantId
    

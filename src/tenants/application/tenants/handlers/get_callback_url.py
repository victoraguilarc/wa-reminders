from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.tenants import GetMembersSiteCallbackBuilderQuery
from src.common.domain.messaging.queries import QueryHandler
from src.tenants.application.tenants.use_cases.callback_builder import CallbackBuilder, MembersSiteCallbackBuilder
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class GetMembersSiteCallbackBuilderHandler(QueryHandler):
    tenant_repository: TenantRepository
    fallback_hostname: str

    def execute(
        self,
        query: GetMembersSiteCallbackBuilderQuery,
    ) -> Optional[CallbackBuilder]:
        return MembersSiteCallbackBuilder(
            tenant_id=query.tenant_id,
            tenant_repository=self.tenant_repository,
            fallback_hostname=self.fallback_hostname,
            sub_path=query.sub_path,
        ).execute()

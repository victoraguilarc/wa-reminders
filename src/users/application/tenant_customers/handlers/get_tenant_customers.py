from dataclasses import dataclass
from typing import List

from src.common.application.queries.users import GetTenantCustomersByIdsQuery
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.messaging.queries import QueryHandler
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class GetTenantCustomersByIdsHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomersByIdsQuery,
    ) -> List[TenantCustomer]:
        return self.repository.filter_by_ids(
            tenant_id=query.tenant_id,
            tenant_customer_ids=query.tenant_customer_ids,
        )

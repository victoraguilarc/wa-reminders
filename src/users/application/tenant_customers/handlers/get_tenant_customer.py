from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import (
    GetTenantCustomerByEmailQuery,
    GetTenantCustomerByIdQuery,
    GetTenantCustomerByParamsQuery,
    GetTenantCustomerByAccessCodeQuery,
    GetTenantCustomerForSessionQuery,
)
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class GetTenantCustomerByEmailHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomerByEmailQuery,
    ) -> Optional[TenantCustomer]:
        tenant_customer = self.repository.find_by_email(
            tenant_id=query.tenant_id,
            email=query.email,
        )


@dataclass
class GetTenantCustomerByIdHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomerByIdQuery,
    ) -> Optional[TenantCustomer]:
        tenant_customer = self.repository.find(
            tenant_id=query.tenant_id,
            tenant_customer_id=query.tenant_customer_id,
        )
        return tenant_customer


@dataclass
class GetTenantCustomerByParamsHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomerByParamsQuery,
    ) -> Optional[TenantCustomer]:
        tenant_customer = self.repository.find_by_params(
            tenant_id=query.tenant_id,
            tenant_customer_id=query.tenant_customer_id,
            email=query.email,
            phone_number=query.phone_number,
        )
        return tenant_customer


@dataclass
class GetTenantCustomerForSessionHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomerForSessionQuery,
    ) -> Optional[TenantCustomer]:
        return self.repository.find_for_session(
            tenant_id=query.tenant_id,
            email=query.email,
            raw_phone_number=query.raw_phone_number,
        )


@dataclass
class GetTenantCustomerByAccessCodeHandler(QueryHandler):
    repository: TenantCustomerRepository

    def execute(
        self,
        query: GetTenantCustomerByAccessCodeQuery,
    ) -> Optional[TenantCustomer]:
        return self.repository.find_by_access_code(
            tenant_id=query.tenant_id,
            access_code=query.access_code,
        )

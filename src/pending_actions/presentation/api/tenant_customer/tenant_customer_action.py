from typing import Optional

from src.common.application.queries.users import GetTenantCustomerForSessionQuery, GetTenantCustomerByIdQuery
from src.common.domain.exceptions.users import TenantCustomerNotFoundError, TenantCustomerNotReachableError
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.value_objects import RawPhoneNumber, TenantCustomerId


class TenantCustomerActionView(object):
    tenant_context = None
    bus_context = None

    def _get_tenant_customer(
        self,
        email: Optional[str] = None,
        raw_phone_number: Optional[RawPhoneNumber] = None,
    ) -> TenantCustomer:
        tenant_customer: Optional[TenantCustomer] = self.bus_context.query_bus.ask(
            query=GetTenantCustomerForSessionQuery(
                tenant_id=self.tenant_context.tenant.id,
                email=email,
                raw_phone_number=raw_phone_number,
            ),
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError

        if not tenant_customer.is_reachable:
            raise TenantCustomerNotReachableError

        return tenant_customer


class TenantCustomerActionByIdView(object):
    tenant_context = None
    bus_context = None

    def _get_tenant_customer(
        self,
        tenant_customer_id: TenantCustomerId,
    ) -> TenantCustomer:
        tenant_customer: Optional[TenantCustomer] = self.bus_context.query_bus.ask(
            query=GetTenantCustomerByIdQuery(
                tenant_id=self.tenant_context.tenant.id,
                tenant_customer_id=tenant_customer_id,
            ),
        )
        if not tenant_customer:
            raise TenantCustomerNotFoundError

        return tenant_customer

    @classmethod
    def _check_reachability(cls, tenant_customer: TenantCustomer):
        if not tenant_customer.is_reachable:
            raise TenantCustomerNotReachableError
        return tenant_customer

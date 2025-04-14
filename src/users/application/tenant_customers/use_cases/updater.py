# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.users.application.mixins import GetTenantCustomerMixin
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class TenantCustomerUpdater(GetTenantCustomerMixin, ApiService):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    updated_instance: TenantCustomer
    updated_fields: List[str]
    repository: TenantCustomerRepository
    command_bus: CommandBus
    run_commands_async: bool = False

    def execute(self, *args, **kwargs) -> TenantCustomer:
        tenant_customer = self.get_tenant_customer(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
        )
        tenant_customer.overload(
            new_instance=self.updated_instance,
            properties=self.updated_fields,
        )
        self._prefix_phone_number(tenant_customer)
        self._check_email_and_phone_uniqueness(
            tenant_customer=tenant_customer,
            excluded_ids=[self.tenant_customer_id],
        )
        # sync tenant customer as customer for payments
        # TODO: Implement this in other service
        # self.command_bus.dispatch(
        #     command=SyncCustomerTenantCustomerCommand(
        #         tenant_id=self.tenant_id,
        #         tenant_customer_id=tenant_customer.id,
        #     ),
        #     run_async=self.run_commands_async,
        # )

        tenant_customer = self.repository.persist(tenant_customer)
        return tenant_customer


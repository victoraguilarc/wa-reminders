# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.enums.users import TenantCustomerStatus
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantId
from src.users.application.mixins import GetTenantCustomerMixin
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


@dataclass
class TenantCustomerCreator(GetTenantCustomerMixin, ApiService):
    tenant_id: TenantId
    new_instance: TenantCustomer
    repository: TenantCustomerRepository
    command_bus: CommandBus
    run_commands_async: bool = False

    def execute(self, *args, **kwargs) -> TenantCustomer:
        self._prefix_phone_number(self.new_instance)
        self._check_email_and_phone_uniqueness(
            tenant_customer=self.new_instance,
        )
        tenant_customer = self.repository.persist(
            instance=self._activate_instance(self.new_instance),
        )
        return tenant_customer

    @classmethod
    def _activate_instance(cls, tenant_customer: TenantCustomer) -> TenantCustomer:
        tenant_customer.status = TenantCustomerStatus.ACTIVE
        return tenant_customer

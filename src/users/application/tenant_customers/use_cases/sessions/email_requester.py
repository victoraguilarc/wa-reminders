from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.common.application.commands.pending_actions import SendEmailSessionRedemptionCommand
from src.common.application.queries.pending_actions import GetTenantCustomerSessionRedemptionQuery
from src.common.constants import DEFAULT_SESSION_REDEMPTION_SUB_PATH
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.common.domain.entities.tenant import Tenant
from src.common.domain.value_objects import TenantCustomerId
from src.users.application.tenant_customers.common.mixins import TenantCustomerCallbackUrlMixin
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerEmailSessionRequester(TenantCustomerCallbackUrlMixin, UseCase):
    tenant: Tenant
    tenant_customer_id: TenantCustomerId
    tenant_customer_repository: TenantCustomerRepository
    command_bus: CommandBus
    query_bus: QueryBus
    run_async_notification: bool = False

    def execute(self) -> Optional[PendingAction]:
        tenant_customer = self.get_tenant_customer()
        if not tenant_customer.email_address:
            logger.warning(
                f'TenantCustomerHasNoEmailAddress: tenant_customer_id={tenant_customer.id}'
            )
            return None

        callback_url = self.get_tenant_customers_callback_url(path=DEFAULT_SESSION_REDEMPTION_SUB_PATH)
        session_redemption: Optional[PendingActionContext] = self.query_bus.ask(
            query=GetTenantCustomerSessionRedemptionQuery(
                tenant_customer=tenant_customer,
                callback_builder=callback_url,
            ),
        )
        self.command_bus.dispatch(
            command=SendEmailSessionRedemptionCommand(
                email=tenant_customer.email,
                tenant_name=self.tenant.name,
                first_name=tenant_customer.first_name,
                action_link=session_redemption.callback_url,
            ),
            run_async=self.run_async_notification,
        )
        return session_redemption.pending_action

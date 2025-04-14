from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.common.application.commands.pending_actions import SendWhatsappSessionRedemptionCommand
from src.common.application.queries.pending_actions import GetTenantCustomerSessionRedemptionQuery
from src.common.constants import DEFAULT_SESSION_REDEMPTION_SUB_PATH
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.users.application.tenant_customers.common.mixins import TenantCustomerCallbackUrlMixin
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerWhatsappSessionRequester(TenantCustomerCallbackUrlMixin, UseCase):
    tenant: Tenant
    tenant_customer_id: TenantCustomerId
    tenant_customer_repository: TenantCustomerRepository
    command_bus: CommandBus
    query_bus: QueryBus
    run_async_notification: bool = False

    def execute(self, *args, **kwargs) -> Optional[PendingAction]:
        tenant_customer = self.get_tenant_customer()
        callback_url = self.get_tenant_customers_callback_url(path=DEFAULT_SESSION_REDEMPTION_SUB_PATH)

        if not tenant_customer.phone_number:
            logger.warning(
                f'TenantCustomerHasNoPhoneNumber: tenant_customer_id={tenant_customer.id}'
            )
            return None

        pending_action = self._send_session_redeption(
            tenant_customer=tenant_customer,
            callback_url=callback_url,
        )
        # self._send_prefixed_session_redemption(
        #     tenant_customer=tenant_customer,
        #     callback_url=callback_url,
        # )
        return pending_action

    def _send_session_redeption(
        self,
        tenant_customer: TenantCustomer,
        callback_url: CallbackBuilder,
    ) -> PendingAction:
        session_redemption: Optional[PendingActionContext] = self.query_bus.ask(
            query=GetTenantCustomerSessionRedemptionQuery(
                tenant_customer=tenant_customer,
                callback_builder=callback_url,
            ),
        )
        self.command_bus.dispatch(
            command=SendWhatsappSessionRedemptionCommand(
                phone_number=tenant_customer.international_number,
                tenant_name=self.tenant.name,
                first_name=tenant_customer.first_name,
                action_link=session_redemption.callback_url,
            ),
            run_async=self.run_async_notification,
        )
        return session_redemption.pending_action

    # def _send_prefixed_session_redemption(
    #     self,
    #     tenant_customer: TenantCustomer,
    #     callback_url: CallbackData,
    # ) -> Optional[PendingAction]:
    #     phone_number = copy.deepcopy(tenant_customer.phone_number)
    #     prefix_context = PhonePrefixContext.from_phone_number(phone_number)
    #     if not prefix_context.has_prefix or phone_number.is_verified:
    #         return None
    #
    #     phone_number.prefix = prefix_context.prefix
    #     session_redemption: Optional[PendingActionContext] = self.query_bus.ask(
    #         query=GetSessionRedemptionQuery(
    #             user=tenant_customer.user,
    #             tenant_id=self.tenant.id,
    #             callback_data=callback_url,
    #             metadata=phone_number.verification_metadata,
    #         ),
    #     )
    #     send_redeem_session_whatsapp(
    #         command_bus=self.command_bus,
    #         phone_number=phone_number.usable_phone_number,
    #         tenant_name=self.tenant.name,
    #         first_name=tenant_customer.first_name,
    #         action_link=session_redemption.callback_url,
    #         run_async=self.run_async,
    #     )
    #     return session_redemption.pending_action

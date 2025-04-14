# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.queries.pending_actions import (
    GetTenantCustomerSessionRedemptionQuery,
)
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.pending_actions.application.use_cases.tenant_customer.session_redemption_generator import (
    TenantCustomerSessionRedemptionGenerator,
)
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class GetTenantCustomerSessionRedemptionHandler(QueryHandler):
    action_repository: PendingActionRepository

    def execute(
        self,
        query: GetTenantCustomerSessionRedemptionQuery,
    ) -> PendingActionContext:
        return TenantCustomerSessionRedemptionGenerator(
            tenant_customer=query.tenant_customer,
            action_repository=self.action_repository,
            callback_builder=query.callback_builder,
            verify_email_address=query.verify_email_address,
            verify_phone_number=query.verify_phone_number,
        ).execute()

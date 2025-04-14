# -*- coding: utf-8 -*-
from dataclasses import dataclass

from src.common.domain.enums.users import PendingActionCategory
from src.common.domain.interfaces.services import ApiService
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.tenant_customer_session_redemption import (
    TenantCustomerSessionRedemption,
)


@dataclass
class TenantCustomerSessionRedemptionGenerator(ApiService):
    tenant_customer: TenantCustomer
    action_repository: PendingActionRepository
    callback_builder: CallbackBuilder
    verify_email_address: bool = False
    verify_phone_number: bool = False

    def execute(self, *args, **kwargs) -> PendingActionContext:
        group_id = self._get_group_id()
        self.action_repository.expire_past_similars(
            group_id=group_id,
            category=PendingActionCategory.TENANT_CUSTOMER_SESSION_REDEMPTION,
        )
        pending_action = self.action_repository.persist_with_token(
            pending_action=PendingAction.tenant_customer_session_redemption(
                group_id=group_id,
                metadata=TenantCustomerSessionRedemption(
                    tenant_id=self.tenant_customer.tenant_id,
                    tenant_customer_id=self.tenant_customer.id,
                    unverified_email_address=(
                        self.tenant_customer.email_address
                        if self.verify_email_address and self.tenant_customer.is_email_unverified
                        else None
                    ),
                    unverified_phone_number=(
                        self.tenant_customer.phone_number
                        if self.verify_phone_number and self.tenant_customer.is_phone_unverified
                        else None
                    ),
                ),
            ),
        )
        return PendingActionContext(
            pending_action=pending_action,
            callback_url=self.callback_builder.build_with_token(
                token=pending_action.token,
            ),
        )

    def _get_group_id(self):
        default_group_id = str(self.tenant_customer.id)
        if self.verify_phone_number:
            default_group_id = f'{default_group_id}-phone-number'
        if self.verify_email_address:
            default_group_id = f'{default_group_id}-email-address'
        return default_group_id


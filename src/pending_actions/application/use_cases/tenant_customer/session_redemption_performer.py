# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.mixins.tenant import GetCurrentTenantMixin
from src.common.application.queries.auth import GetUserSessionTokenQuery
from src.common.application.queries.users import GetTenantCustomerByIdQuery
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.user import User
from src.common.domain.entities.user_session import TenantCustomerSession
from src.common.domain.value_objects import UserSessionToken
from src.pending_actions.application.use_cases.mixins import (
    PerformVerificationsMixin,
    UpdatePendingActionMixin,
)
from src.pending_actions.domain.exceptions import (
    InvalidPendingActionError,
    CorruptedPendingActionError,
)
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.tenant_customer_session_redemption import (
    TenantCustomerSessionRedemption,
)


@dataclass
class TenantCustomerSessionRedemptionPerformer(
    UpdatePendingActionMixin,
    GetCurrentTenantMixin,
    PerformVerificationsMixin,
    UseCase,
):
    command_bus: CommandBus
    pending_action: PendingAction
    action_repository: PendingActionRepository

    def execute(self) -> TenantCustomerSession:
        self._validate_pending_action()
        metadata = self._build_metadata(self.pending_action)
        tenant_customer = self._get_tenant_customer(metadata)
        self._perform_included_verifications(self.pending_action)
        self._update_pending_action(self.pending_action)

        return TenantCustomerSession(
            profile=tenant_customer,
            token=self._get_user_session_token(tenant_customer.user),
            current_tenant=self.get_current_tenant(tenant_customer.user),
        )

    def _validate_pending_action(self):
        if self.pending_action.is_tenant_customer_session_redemption and self.pending_action.is_actionable:
            return
        raise InvalidPendingActionError


    def _get_tenant_customer(
        self,
        metadata: TenantCustomerSessionRedemption,
    ) -> Optional[TenantCustomer]:
        tenant_customer: Optional[TenantCustomer] = self.query_bus.ask(
            query=GetTenantCustomerByIdQuery(
                tenant_id=metadata.tenant_id,
                tenant_customer_id=metadata.tenant_customer_id,
            ),
        )
        if not tenant_customer:
            raise CorruptedPendingActionError
        return tenant_customer

    def _get_user_session_token(self, user: User) -> Optional[UserSessionToken]:
        return self.query_bus.ask(
            query=GetUserSessionTokenQuery(user=user),
        )

    @classmethod
    def _build_metadata(cls, pending_action: PendingAction):
        return TenantCustomerSessionRedemption.from_dict(
            data=pending_action.metadata,
        )

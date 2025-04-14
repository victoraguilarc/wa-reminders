# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.users import (
    PersistTenantUserCommand,
    PersistEmailAddressCommand, SetUserPasswordCommand,
)
from src.common.application.queries.users import GetTenantUserByIdQuery
from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant_user import TenantUser
from src.pending_actions.application.use_cases.mixins import (
    PerformVerificationsMixin,
    UpdatePendingActionMixin,
)
from src.pending_actions.domain.exceptions import (
    InvalidPendingActionError,
    CorruptedPendingActionError,
)
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.tenant_user_invitation import TenantUserInvitation


@dataclass
class TenantUserInvitationPerformer(
    UpdatePendingActionMixin,
    PerformVerificationsMixin,
    UseCase,
):
    pending_action: PendingAction
    action_repository: PendingActionRepository
    command_bus: CommandBus
    query_bus: QueryBus
    password: Optional[str] = None
    user_person: Optional[SimplePerson] = None

    def execute(self) -> PendingActionResult:
        self._validate_pending_action()
        action_metadata = self._build_action_metadata(self.pending_action)
        tenant_user = self._get_tenant_user(action_metadata)

        self._update_tenant_user(tenant_user)
        self._update_password(tenant_user)
        pending_action = self._update_pending_action(self.pending_action)

        return PendingActionResult(
            pending_action=pending_action,
            status=TaskResultStatus.SUCCESS,
        )

    def _validate_pending_action(self):
        if self.pending_action.is_tenant_user_invitation and self.pending_action.is_actionable:
            return
        raise InvalidPendingActionError

    def _process_status(self, pending_action: PendingAction):
        pending_action.increment_usage()
        if pending_action.is_usage_limit_reached:
            self.action_repository.complete(pending_action)
        self.action_repository.persist(pending_action)

    def _get_tenant_user(
        self,
        action_metadata: TenantUserInvitation,
    ) -> Optional[TenantUser]:
        tenant_customer: Optional[TenantUser] = self.query_bus.ask(
            query=GetTenantUserByIdQuery(
                tenant_id=action_metadata.tenant_id,
                tenant_user_id=action_metadata.tenant_user_id,
            ),
        )
        if not tenant_customer:
            raise CorruptedPendingActionError
        return tenant_customer

    def _update_tenant_user(self, tenant_user: TenantUser):
        if self.user_person:
            tenant_user.first_name = self.user_person.first_name
            tenant_user.paternal_surname = self.user_person.paternal_surname
            tenant_user.maternal_surname = self.user_person.maternal_surname

        tenant_user.activate()

        self.command_bus.dispatch(
            command=PersistTenantUserCommand(tenant_user),
        )
        if tenant_user.user.email_address.is_verified:
            return

        tenant_user.user.email_address.verify()
        self.command_bus.dispatch(
            command=PersistEmailAddressCommand(tenant_user.user.email_address),
        )

    def _update_password(self, tenant_user: TenantUser):
        if not self.password:
            return
        self.command_bus.dispatch(
            command=SetUserPasswordCommand(
                user_id=tenant_user.user.id,
                new_password=self.password,
            ),
        )


    @classmethod
    def _build_action_metadata(
        cls,
        pending_action: PendingAction,
    ) -> TenantUserInvitation:
        return TenantUserInvitation.from_dict(
            data=pending_action.metadata,
        )






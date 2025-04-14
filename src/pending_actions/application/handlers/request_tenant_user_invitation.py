from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.pending_actions import (
    RequestTenantUserInvitationCommand,
)
from src.common.application.queries.users import GetTenantUserByIdQuery
from src.common.domain.messaging.commands import CommandBus, CommandHandler
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import TenantUserId, TenantId
from src.common.presentation.helpers.callback_builder import get_composed_callback_builder
from src.pending_actions.application.use_cases.tenant_user.invitation_generator import (
    TenantUserInvitationGenerator,
)
from src.pending_actions.application.use_cases.tenant_user.invitation_notifier import (
    TenantUserInvitationNotifier,
)
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class RequestTenantUserInvitationHandler(CommandHandler):
    command_bus: CommandBus
    query_bus: QueryBus
    pending_action_repository: PendingActionRepository

    def execute(
        self,
        command: RequestTenantUserInvitationCommand,
    ):
        tenant_user = self._get_tenant_user(
            tenant_id=command.tenant_id,
            tenant_user_id=command.tenant_user_id,
        )
        action_context = TenantUserInvitationGenerator(
            tenant_user=tenant_user,
            action_repository=self.pending_action_repository,
            callback_builder=get_composed_callback_builder(
                view_name='views:pending-actions:tenant-user-invitation',
            ),
        ).execute()
        TenantUserInvitationNotifier(
            tenant_user=tenant_user,
            command_bus=self.command_bus,
            callback_url=action_context.callback_url,
        ).execute()

    def _get_tenant_user(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
    ) -> Optional[TenantUser]:
        return self.query_bus.ask(
            query=GetTenantUserByIdQuery(
                tenant_id=tenant_id,
                tenant_user_id=tenant_user_id,
            ),
        )

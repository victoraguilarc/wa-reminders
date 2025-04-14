# -*- coding: utf-8 -*-
from dataclasses import dataclass

from src.common.domain.enums.users import PendingActionCategory
from src.common.domain.interfaces.services import ApiService
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.common.domain.entities.tenant_user import TenantUser
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.tenant_user_invitation import TenantUserInvitation


@dataclass
class TenantUserInvitationGenerator(ApiService):
    tenant_user: TenantUser
    action_repository: PendingActionRepository
    callback_builder: CallbackBuilder

    def execute(self) -> PendingActionContext:
        group_id = str(self.tenant_user.id)
        self.action_repository.expire_past_similars(
            group_id=group_id,
            category=PendingActionCategory.TENANT_USER_INVITATION,
        )
        pending_action = self.action_repository.persist_with_token(
            pending_action=PendingAction.tenant_user_invitation(
                group_id=group_id,
                metadata=TenantUserInvitation(
                    tenant_id=self.tenant_user.tenant_id,
                    tenant_user_id=self.tenant_user.id,
                    email=self.tenant_user.email,
                ),
            ),
        )
        return PendingActionContext(
            pending_action=pending_action,
            callback_url=self.callback_builder.build_with_token(
                token=pending_action.token,
            ),
        )

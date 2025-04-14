# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.enums.users import PendingActionCategory
from src.common.domain.interfaces.services import ApiService
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_context import PendingActionContext
from src.common.domain.models.user import User
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.user_reset_password import UserResetPassword


@dataclass
class UserResetPasswordGenerator(ApiService):
    user: User
    action_repository: PendingActionRepository
    callback_builder: CallbackBuilder

    def execute(self) -> PendingActionContext:
        group_id = self.user.email or str(self.user.id)
        self.action_repository.expire_past_similars(
            group_id=group_id,
            category=PendingActionCategory.USER_RESET_PASSWORD,
        )
        pending_action = self.action_repository.persist_with_token(
            pending_action=PendingAction.user_reset_password(
                group_id=group_id,
                metadata=UserResetPassword(
                    user_id=self.user.id,
                    email=self.user.email,
                ),
            ),
        )
        return PendingActionContext(
            pending_action=pending_action,
            callback_url=self.callback_builder.build_with_token(
                token=pending_action.token,
            ),
        )


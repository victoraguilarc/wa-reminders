# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.users import SetUserPasswordCommand
from src.common.application.queries.users import GetUserByIdQuery
from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.common.domain.models.user import User
from src.pending_actions.application.use_cases.mixins import UpdatePendingActionMixin
from src.pending_actions.domain.exceptions import InvalidPendingActionError, CorruptedPendingActionError
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.user_reset_password import UserResetPassword


@dataclass
class UserResetPasswordPerformer(
    UpdatePendingActionMixin,
    UseCase,
):
    pending_action: PendingAction
    new_password: str
    action_repository: PendingActionRepository
    query_bus: QueryBus
    command_bus: CommandBus

    def execute(self) -> PendingActionResult:
        self._validate_pending_action()
        action_metadata = self._build_action_metadata(self.pending_action)
        user = self._get_user(action_metadata)
        self._update_password(user)
        pending_action = self._update_pending_action(self.pending_action)

        return PendingActionResult(
            status=TaskResultStatus.SUCCESS,
            pending_action=pending_action,
        )

    def _validate_pending_action(self):
        if self.pending_action.is_user_reset_password and self.pending_action.is_actionable:
            return
        raise InvalidPendingActionError

    def _get_user(
        self,
        action_metadata: UserResetPassword,
    ) -> Optional[User]:
        user: Optional[User] = self.query_bus.ask(
            query=GetUserByIdQuery(user_id=action_metadata.user_id),
        )
        if not user:
            raise CorruptedPendingActionError
        return user

    def _update_password(self, user: User):
        self.command_bus.dispatch(
            command=SetUserPasswordCommand(
                user_id=user.id,
                new_password=self.new_password,
            ),
        )

    @classmethod
    def _build_action_metadata(
        cls,
        pending_action: PendingAction,
    ) -> UserResetPassword:
        return UserResetPassword.from_dict(
            data=pending_action.metadata,
        )

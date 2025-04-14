# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.auth.domain.repositories.session_user import SessionUserRepository
from src.common.application.queries.pending_actions import GetEmailAddressVerificationQuery
from src.common.domain.exceptions.common import EmailIsAlreadyUsedError
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_context import PendingActionContext
from src.common.domain.models.user import User
from src.pending_actions.domain.callback_builder import CallbackBuilder


@dataclass
class UserRegister(ApiService):
    user_instance: User
    raw_password: str
    session_user_repository: SessionUserRepository
    query_bus: QueryBus
    callback_builder: CallbackBuilder
    send_async_email: bool

    def execute(
        self,
    ) -> PendingAction:
        existent_user = self.session_user_repository.find_by_email(
            email=self.user_instance.email,
        )
        if existent_user:
            raise EmailIsAlreadyUsedError

        new_user = self.session_user_repository.register(
            user=self.user_instance,
            raw_password=self.raw_password,
        )
        action_context = self._get_action_context(email=new_user.email)
        return action_context.pending_action

    def _get_action_context(self, email: str) -> Optional[PendingActionContext]:
        return self.query_bus.ask(
            query=GetEmailAddressVerificationQuery(
                email=email,
                callback_builder=self.callback_builder,
                send_async_email=self.send_async_email,
            ),
        )

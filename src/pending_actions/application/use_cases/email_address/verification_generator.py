# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import GetOrCreateEmailAddressQuery
from src.common.domain.enums.users import PendingActionCategory
from src.common.domain.exceptions.auth import EmailAddressIsAlreadyVerifiedError
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_context import PendingActionContext
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.email_address_verification import EmailAddressVerification


@dataclass
class EmailAddressVerificationGenerator(UseCase):
    email: str
    query_bus: QueryBus
    action_repository: PendingActionRepository
    callback_builder: CallbackBuilder

    def execute(self) -> PendingActionContext:
        email_address = self._get_or_create_email_address()

        self._validate_needs_verification(email_address)
        self.action_repository.expire_past_similars(
            group_id=self.email,
            category=PendingActionCategory.EMAIL_ADDRESS_VERIFICATION,
        )
        pending_action = self.action_repository.persist_with_token(
            pending_action=PendingAction.email_address_verification(
                group_id=self.email,
                metadata=EmailAddressVerification(
                    email_address_id=email_address.id,
                    email=email_address.email,
                ),
            ),
        )
        return PendingActionContext(
            pending_action=pending_action,
            callback_url=self.callback_builder.build_with_token(
                token=pending_action.token,
            ),
        )

    def _get_or_create_email_address(self) -> Optional[EmailAddress]:
        return self.query_bus.ask(
            query=GetOrCreateEmailAddressQuery(email=self.email),
        )

    @classmethod
    def _validate_needs_verification(cls, email_address):
        if not email_address.is_verified:
            return
        raise EmailAddressIsAlreadyVerifiedError



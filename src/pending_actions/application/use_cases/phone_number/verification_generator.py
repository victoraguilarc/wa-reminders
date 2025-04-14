# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import GetOrCreatePhoneNumberQuery
from src.common.domain.enums.users import PendingActionCategory
from src.common.domain.exceptions.auth import PhoneNumberIsAlreadyVerifiedError
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_context import PendingActionContext
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.value_objects import RawPhoneNumber
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.phone_number_verification import PhoneNumberVerification


@dataclass
class PhoneNumberVerificationGenerator(UseCase):
    raw_phone_number: RawPhoneNumber
    action_repository: PendingActionRepository
    query_bus: QueryBus
    callback_builder: CallbackBuilder

    def execute(self) -> PendingActionContext:
        phone_number = self._get_or_create_phone_number()
        self._validate_needs_verification(phone_number)
        self.action_repository.expire_past_similars(
            group_id=self.raw_phone_number.international_number,
            category=PendingActionCategory.PHONE_NUMBER_VERIFICATION,
        )
        pending_action = self.action_repository.persist_with_token(
            pending_action=PendingAction.phone_number_verification(
                group_id=self.raw_phone_number.international_number,
                metadata=PhoneNumberVerification(
                    phone_number_id=phone_number.id,
                    raw_phone_number=self.raw_phone_number,
                ),
            ),
        )
        return PendingActionContext(
            pending_action=pending_action,
            callback_url=self.callback_builder.build_with_token(
                token=pending_action.token,
            ),
        )

    def _get_or_create_phone_number(self) -> Optional[PhoneNumber]:
        return self.query_bus.ask(
            query=GetOrCreatePhoneNumberQuery(
                raw_phone_number=self.raw_phone_number,
            ),
        )

    @classmethod
    def _validate_needs_verification(cls, phone_number: PhoneNumber):
        if not phone_number.is_verified:
            return
        raise PhoneNumberIsAlreadyVerifiedError




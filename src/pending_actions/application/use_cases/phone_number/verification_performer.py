# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.users import PersistPhoneNumberCommand
from src.common.application.queries.users import GetOrCreatePhoneNumberQuery
from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.entities.pending_action_result import PendingActionResult
from src.common.domain.entities.phone_number import PhoneNumber
from src.pending_actions.application.use_cases.mixins import UpdatePendingActionMixin
from src.pending_actions.application.use_cases.update_publisher import (
    PendingActionSSEventPublisher,
)
from src.pending_actions.domain.exceptions import CorruptedPendingActionError, InvalidPendingActionError
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.phone_number_verification import PhoneNumberVerification


@dataclass
class PhoneNumberVerificationPerformer(UpdatePendingActionMixin, UseCase):
    pending_action: PendingAction
    action_repository: PendingActionRepository
    stream_events_publisher: StreamEventPublisher
    command_bus: CommandBus
    query_bus: QueryBus

    def execute(self) -> PendingActionResult:
        self._validate_pending_action()
        metadata = self._build_metadata(self.pending_action)
        self._update_phone_number(metadata)
        pending_action = self._update_pending_action(self.pending_action)
        self._publish_event(pending_action)

        return PendingActionResult(
            pending_action=pending_action,
            status=TaskResultStatus.SUCCESS,
        )

    def _validate_pending_action(self):
        if self.pending_action.is_phone_verification and self.pending_action.is_actionable:
            return
        raise InvalidPendingActionError

    def _update_phone_number(self, metadata: PhoneNumberVerification):
        phone_number: Optional[PhoneNumber] = self.query_bus.ask(
            query=GetOrCreatePhoneNumberQuery(
                raw_phone_number=metadata.raw_phone_number,
            ),
        )

        if phone_number.is_verified:
            return

        phone_number.is_verified = True
        self.command_bus.dispatch(command=PersistPhoneNumberCommand(phone_number))

    def _publish_event(self, pending_action: PendingAction):
        PendingActionSSEventPublisher(
            pending_action=pending_action,
            stream_events_publisher=self.stream_events_publisher,
        ).execute()

    @classmethod
    def _build_metadata(cls, pending_action):
        metadata = PhoneNumberVerification.from_dict(pending_action.metadata)
        if not metadata.is_valid:
            raise CorruptedPendingActionError
        return metadata

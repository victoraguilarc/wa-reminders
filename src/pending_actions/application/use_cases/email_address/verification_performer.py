# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.application.commands.users import PersistEmailAddressCommand
from src.common.application.queries.users import GetOrCreateEmailAddressQuery
from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.pending_actions.application.use_cases.mixins import UpdatePendingActionMixin
from src.pending_actions.application.use_cases.update_publisher import (
    PendingActionSSEventPublisher,
)
from src.pending_actions.domain.exceptions import CorruptedPendingActionError, InvalidPendingActionError
from src.pending_actions.domain.repositories import PendingActionRepository
from src.pending_actions.domain.types.email_address_verification import EmailAddressVerification


@dataclass
class EmailAddressVerificationPerformer(UpdatePendingActionMixin, UseCase):
    pending_action: PendingAction
    action_repository: PendingActionRepository
    stream_events_publisher: StreamEventPublisher
    command_bus: CommandBus
    query_bus: QueryBus

    def execute(self) -> PendingActionResult:
        self._validate_pending_action()
        metadata = self._build_metadata(self.pending_action)
        self._update_email_address(metadata)
        pending_action = self._update_pending_action(self.pending_action)
        self._publish_event(pending_action)

        return PendingActionResult(
            pending_action=pending_action,
            status=TaskResultStatus.SUCCESS,
        )

    def _validate_pending_action(self):
        if self.pending_action.is_email_verification and self.pending_action.is_actionable:
            return
        raise InvalidPendingActionError

    def _update_email_address(self, metadata: EmailAddressVerification):
        email_address: Optional[EmailAddress] = self.query_bus.ask(
            query=GetOrCreateEmailAddressQuery(
                email=metadata.email,
            ),
        )

        if email_address.is_verified:
            return

        email_address.verify()
        self.command_bus.dispatch(command=PersistEmailAddressCommand(email_address))

    def _publish_event(self, pending_action: PendingAction):
        PendingActionSSEventPublisher(
            pending_action=pending_action,
            stream_events_publisher=self.stream_events_publisher,
        ).execute()


    @classmethod
    def _build_metadata(cls, pending_action):
        metadata = EmailAddressVerification.from_dict(pending_action.metadata)
        if not metadata.is_valid:
            raise CorruptedPendingActionError
        return metadata



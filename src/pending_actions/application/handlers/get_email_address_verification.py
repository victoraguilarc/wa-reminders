from dataclasses import dataclass

from src.common.application.queries.pending_actions import GetEmailAddressVerificationQuery
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryHandler, QueryBus
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.pending_actions.application.use_cases.email_address.verification_generator import (
    EmailAddressVerificationGenerator,
)
from src.pending_actions.application.use_cases.email_address.verification_notifier import (
    EmailAddressVerificationNotifier
)
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class GetEmailAddressVerificationHandler(QueryHandler):
    action_repository: PendingActionRepository
    query_bus: QueryBus
    command_bus: CommandBus

    def execute(
        self,
        query: GetEmailAddressVerificationQuery,
    ) -> PendingActionContext:

        action_context = EmailAddressVerificationGenerator(
            email=query.email,
            action_repository=self.action_repository,
            callback_builder=query.callback_builder,
            query_bus=self.query_bus,
        ).execute()

        EmailAddressVerificationNotifier(
            email=query.email,
            command_bus=self.command_bus,
            callback_url=action_context.callback_url,
            send_async_email=query.send_async_email,
        ).execute()

        return action_context

from dataclasses import dataclass

from src.common.application.queries.pending_actions import GetPhoneNumberVerificationQuery
from src.common.domain.messaging.queries import QueryHandler, QueryBus
from src.common.domain.entities.pending_action_context import PendingActionContext
from src.pending_actions.application.use_cases.phone_number.verification_generator import (
    PhoneNumberVerificationGenerator,
)
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class GetPhoneNumberVerificationHandler(QueryHandler):
    action_repository: PendingActionRepository
    query_bus: QueryBus

    def execute(
        self,
        query: GetPhoneNumberVerificationQuery,
    ) -> PendingActionContext:
        return PhoneNumberVerificationGenerator(
            group_id=query.group_id,
            raw_phone_number=query.raw_phone_number,
            action_repository=self.action_repository,
            callback_builder=query.callback_builder,
            query_bus=self.query_bus,
        ).execute()

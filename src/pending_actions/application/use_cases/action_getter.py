from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase
from src.common.domain.models.pending_action import PendingAction
from src.pending_actions.domain.exceptions import PendingActionNotFoundError
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class PendingActionGetter(UseCase):
    token_or_tracking_code: str
    action_repository: PendingActionRepository

    def execute(self) -> PendingAction:
        pending_action = self.action_repository.find(
            token_or_tracking_code=self.token_or_tracking_code,
        )
        if not pending_action:
            raise PendingActionNotFoundError
        return pending_action

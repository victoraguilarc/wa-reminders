from dataclasses import dataclass
from typing import Optional

from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.entities.pending_action import PendingAction
from src.pending_actions.domain.exceptions import InvalidPendingActionError
from src.pending_actions.domain.repositories import PendingActionRepository


@dataclass
class PendingActionTokenGetter(UseCase):
    token: str
    category: PendingActionCategory
    status: PendingActionStatus
    action_repository: PendingActionRepository
    raise_exception: bool = True

    def execute(self, *args, **kwargs) -> Optional[PendingAction]:
        pending_action: Optional[PendingAction] = self.action_repository.find_by_token(
            token=self.token,
            category=self.category,
            status=self.status,
        )

        if not pending_action and self.raise_exception:
            raise InvalidPendingActionError

        return pending_action



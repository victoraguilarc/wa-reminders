from dataclasses import dataclass
from typing import Optional

from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.models.pending_action import PendingAction


@dataclass
class PendingActionResult(object):
    pending_action: Optional[PendingAction]
    status: TaskResultStatus

    @property
    def is_success(self) -> bool:
        return self.status == TaskResultStatus.SUCCESS

    @property
    def is_completed(self) -> bool:
        return (
            self.pending_action is not None
            and self.status == TaskResultStatus.SUCCESS
        )

    @property
    def is_in_progress(self) -> bool:
        return self.status == TaskResultStatus.IN_PROGRESS

    @classmethod
    def failure(cls) -> 'PendingActionResult':
        return cls(
            pending_action=None,
            status=TaskResultStatus.FAILURE,
        )

    @classmethod
    def success(cls, pending_action: PendingAction) -> 'PendingActionResult':
        return cls(
            pending_action=pending_action,
            status=TaskResultStatus.FAILURE,
        )

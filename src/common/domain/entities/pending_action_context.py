from dataclasses import dataclass

from src.common.domain.entities.pending_action import PendingAction


@dataclass
class PendingActionContext(object):
    pending_action: PendingAction
    callback_url: str

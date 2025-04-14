from dataclasses import dataclass
from typing import Dict

from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.enums.auth import PendingActionNamespace
from src.common.domain.interfaces.services import UseCase


@dataclass
class PendingActionUrlBuilder(UseCase):
    pending_action: PendingAction
    namespace: PendingActionNamespace
    hostnames_map: Dict[PendingActionNamespace, CallbackBuilder]
    default_token_path: CallbackBuilder

    def execute(self, *args, **kwargs):
        token_path: CallbackBuilder = self.hostnames_map.get(self.namespace, self.default_token_path)
        return token_path.build_with_token(self.pending_action.token)

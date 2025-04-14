from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase


@dataclass
class ReminderProcessor(UseCase):
    def execute(self, *args, **kwargs):
        pass

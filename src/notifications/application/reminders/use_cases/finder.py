from dataclasses import dataclass

from src.common.domain.interfaces.services import UseCase


@dataclass
class ReminderFinder(UseCase):
    def execute(self, *args, **kwargs):
        pass

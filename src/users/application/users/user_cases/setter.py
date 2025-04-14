from dataclasses import dataclass

from src.common.domain.entities.user import User
from src.common.domain.interfaces.services import UseCase
from src.users.domain.repositories.user import UserRepository


@dataclass
class UserSetter(UseCase):
    instance: User
    raw_password: str
    repository: UserRepository

    def execute(self):
        created_instance = self.repository.register(self.instance)
        self.repository.set_password(
            user_id=created_instance.id,
            new_password=self.raw_password,
        )

from dataclasses import dataclass
from typing import Optional

from src.common.application.queries.users import GetUserByEmailQuery, GetUserByIdQuery
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.models.user import User
from src.users.domain.repositories.user import UserRepository


@dataclass
class GetUserByEmailHandler(QueryHandler):
    repository: UserRepository

    def execute(self, query: GetUserByEmailQuery) -> Optional[User]:
        return self.repository.find_by_email(email=query.email)


@dataclass
class GetUserByIdHandler(QueryHandler):
    repository: UserRepository

    def execute(self, query: GetUserByIdQuery) -> Optional[User]:
        return self.repository.find(
            user_id=query.user_id,
        )

from dataclasses import dataclass

from src.auth.domain.interfaces import UserSessionTokenBuilder
from src.common.application.queries.auth import GetUserSessionTokenQuery
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.value_objects import UserSessionToken


@dataclass
class GetUserSessionTokenHandler(QueryHandler):
    token_builder: UserSessionTokenBuilder

    def execute(self, query: GetUserSessionTokenQuery) -> UserSessionToken:
        return self.token_builder.make_token(query.user)

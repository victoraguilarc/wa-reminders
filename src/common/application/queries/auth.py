from dataclasses import dataclass

from src.common.domain.messaging.queries import Query
from src.common.domain.entities.user import User


@dataclass
class GetUserSessionTokenQuery(Query):
    user: User

from typing import Optional

from src.common.application.queries.users import GetUserByEmailQuery
from src.common.domain.exceptions.users import UserNotFoundError
from src.common.domain.entities.user import User


class UserActionView(object):
    bus_context = None
    tenant_context = None
    def _get_user(
        self,
        email: str,
    ) -> Optional[User]:
        user: Optional[User] = self.bus_context.query_bus.ask(
            query=GetUserByEmailQuery(
                email=email,
            ),
        )
        if not user:
            raise UserNotFoundError
        return user


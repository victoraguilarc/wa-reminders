from dataclasses import dataclass

from src.common.application.queries.users import GetOrCreateEmailAddressQuery
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.models.email_address import EmailAddress
from src.users.domain.repositories.email_address import EmailAddressRepository


@dataclass
class GetOrCreateEmailAddressHandler(QueryHandler):
    repository: EmailAddressRepository

    def execute(
        self,
        query: GetOrCreateEmailAddressQuery,
    ) -> EmailAddress:
        return self.repository.get_or_create(email=query.email)




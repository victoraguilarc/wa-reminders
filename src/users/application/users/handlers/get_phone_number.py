from dataclasses import dataclass

from src.common.application.queries.users import GetOrCreatePhoneNumberQuery
from src.common.domain.messaging.queries import QueryHandler
from src.common.domain.models.phone_number import PhoneNumber
from src.users.domain.repositories.phone_number import PhoneNumberRepository


@dataclass
class GetOrCreatePhoneNumberHandler(QueryHandler):
    repository: PhoneNumberRepository

    def execute(
        self,
        query: GetOrCreatePhoneNumberQuery,
    ) -> PhoneNumber:
        return self.repository.get_or_create(
            raw_phone_number=query.raw_phone_number,
        )



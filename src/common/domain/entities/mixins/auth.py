from dataclasses import dataclass
from typing import Optional

from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.phone_number import PhoneNumber


@dataclass
class DomainAuthMixin(object):
    phone_number: Optional[PhoneNumber]
    email_address: Optional[EmailAddress]

    @property
    def display_email(self) -> str:
        return self.email_address.email if self.email_address else '---'

    @property
    def display_phone(self) -> str:
        return self.phone_number.display_phone if self.phone_number else '---'

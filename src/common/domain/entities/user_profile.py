from dataclasses import dataclass
from typing import Optional, Union
from uuid import UUID

from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.mixins.profile import DomainProfileMixin
from src.common.domain.entities.phone_number import PhoneNumber


@dataclass
class UserProfile(DomainProfileMixin):
    id: Optional[Union[str, UUID]]
    user_id: Optional[Union[str, UUID]]
    email_address: Optional[EmailAddress]
    phone_number: Optional[PhoneNumber]

    @property
    def display_email(self) -> str:
        return self.email_address.email if self.email_address else '---'

    @property
    def display_phone(self) -> str:
        return self.phone_number.display_phone if self.phone_number else '---'

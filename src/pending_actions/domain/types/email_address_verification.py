from dataclasses import dataclass

from src.common.domain.value_objects import EmailAddressId


@dataclass
class EmailAddressVerification(object):
    email: str
    email_address_id: EmailAddressId

    @property
    def to_dict(self):
        return {
            'email_address_id': str(self.email_address_id),
            'email': self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            email_address_id=EmailAddressId(data.get('email_address_id')),
            email=data.get('email'),
        )

    @property
    def is_valid(self):
        return bool(self.email_address_id and self.email)

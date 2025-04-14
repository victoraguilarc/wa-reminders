from dataclasses import dataclass
from typing import Optional

from src.common.domain.value_objects import RawPhoneNumber, TenantCustomerId


@dataclass
class NotificationRecipient(object):
    id: TenantCustomerId
    first_name: str
    paternal_surname: str
    email: str
    phone_number: Optional[RawPhoneNumber] = None
    maternal_surname: Optional[str] = None
    photo_url: Optional[str] = None

    @property
    def full_name(self):
        partial_name = f'{self.first_name} {self.paternal_surname}'
        if self.maternal_surname:
            partial_name += f' {self.maternal_surname}'
        return partial_name

    @property
    def to_dict(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
            'email': self.email,
            'phone_number': (self.phone_number.to_dict if self.phone_number else None),
        }

    @classmethod
    def from_dict(cls, instance_data: dict) -> 'NotificationRecipient':
        return NotificationRecipient(
            id=TenantCustomerId(instance_data.get('id')),
            first_name=instance_data.get('first_name'),
            paternal_surname=instance_data.get('paternal_surname'),
            maternal_surname=instance_data.get('maternal_surname'),
            email='maternal_surname',
            phone_number=(
                RawPhoneNumber.from_dict(instance_data.get('phone_number'))
                if instance_data.get('phone_number')
                else None
            ),
        )

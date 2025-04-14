# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.value_objects import RawPhoneNumber


@dataclass
class SimplePerson(object):
    first_name: Optional[str] = None
    paternal_surname: Optional[str] = None
    maternal_surname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[RawPhoneNumber] = None

    @property
    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'first_name': self.first_name,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
            'phone_number': (self.phone_number.to_dict if self.phone_number else None),
        }

    @property
    def is_enrollable(self) -> bool:
        return self.email and self.first_name is not None and self.paternal_surname is not None

    @classmethod
    def from_dict(cls, instance_data: dict) -> 'SimplePerson':
        return cls(
            email=instance_data.get('email'),
            first_name=instance_data.get('first_name'),
            paternal_surname=instance_data.get('paternal_surname'),
            maternal_surname=instance_data.get('maternal_surname'),
            phone_number=(
                RawPhoneNumber.from_dict(instance_data.get('phone_number'))
                if instance_data.get('phone_number')
                else None
            ),
        )

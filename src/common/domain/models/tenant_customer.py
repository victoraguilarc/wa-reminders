# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import Gender, TenantCustomerStatus, TenantCustomerCreationSource
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.mixins.auth import DomainAuthMixin
from src.common.domain.models.mixins.profile import DomainProfileMixin
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.user import User
from src.common.domain.models.user_profile import UserProfile
from src.common.domain.value_objects import TenantCustomerId, TenantId, RawPhoneNumber
from src.common.helpers.dicts import validate_mandatory


@dataclass
class TenantCustomer(DomainProfileMixin, DomainAuthMixin, AggregateRoot):
    id: TenantCustomerId
    tenant_id: TenantId
    user: User
    status: TenantCustomerStatus
    creation_source: TenantCustomerCreationSource
    created_at: Optional[datetime] = None

    has_memberships: bool = False


    def __eq__(self, other: 'TenantCustomer'):
        return self.id == other.id

    @property
    def raw_phone_number(self) -> Optional[RawPhoneNumber]:
        if not self.phone_number:
            return None
        return self.phone_number.raw_phone_number

    @property
    def is_active(self) -> bool:
        return self.status.is_active

    @property
    def is_inactive(self) -> bool:
        return self.status.is_inactive

    @property
    def is_lead(self) -> bool:
        return self.status.is_lead

    @property
    def email(self) -> Optional[str]:
        return self.email_address.email if self.email_address else None

    @property
    def phone(self) -> Optional[str]:
        return self.phone_number.display_phone if self.phone_number else None

    @property
    def display_email(self) -> Optional[str]:
        return self.email or '---'

    @property
    def display_phone(self) -> Optional[str]:
        return self.phone or '---'

    @property
    def international_number(self) -> Optional[str]:
        if not self.phone_number:
            return None
        return self.phone_number.international_number

    @property
    def is_email_reachable(self) -> bool:
        return self.email_address and self.email_address.is_verified

    @property
    def is_email_unverified(self) -> bool:
        return self.email_address and not self.email_address.is_verified

    @property
    def is_phone_number_reachable(self) -> bool:
        return self.phone_number and self.phone_number.is_verified

    @property
    def is_phone_unverified(self) -> bool:
        return self.phone_number and not self.phone_number.is_verified

    @property
    def is_reachable(self) -> bool:
        return self.is_email_reachable or self.is_phone_number_reachable

    @property
    def email_verification_metadata(self) -> dict:
        metadata = dict()
        if self.email_address and not self.email_address.is_verified:
            metadata['email_address'] = self.email_address.to_dict
        return metadata

    @property
    def phone_verification_metadata(self) -> dict:
        metadata = dict()
        if self.phone_number and not self.phone_number.is_verified:
            metadata['phone_number'] = self.phone_number.to_dict
        return metadata

    @property
    def verification_metadata(self) -> dict:
        return {
            **self.email_verification_metadata,
            **self.phone_verification_metadata,
        }

    @property
    def profile(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            user_id=self.user.id,
            email_address=self.email_address,
            phone_number=self.user.phone_number,
            first_name=self.first_name,
            paternal_surname=self.paternal_surname,
            maternal_surname=self.maternal_surname,
            photo_url=self.photo_url,
            photo=None,
            lang=self.lang,
            birth_date=self.birth_date,
            gender=self.gender,
        )

    @property
    def to_simple_person(self) -> SimplePerson:
        return SimplePerson(
            email=self.email_address.email if self.email_address else None,
            first_name=self.first_name,
            paternal_surname=self.paternal_surname,
            maternal_surname=self.maternal_surname,
        )

    @property
    def channel_id(self) -> str:
        return f'{self.__class__.__name__}@{self.id}'


    @property
    def to_simple_dict(self) -> dict:
        return {
            'id': str(self.id),
            'email': self.email_address.email if self.email_address else None,
            'first_name': self.first_name,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
        }

    @property
    def is_new(self) -> bool:
        return self.created_at is None

    @classmethod
    def build_channel_id(cls, tenant_customer_id: TenantCustomerId) -> str:
        return f'{cls.__name__}@{tenant_customer_id}'

    @classmethod
    def from_payload(cls, verified_data) -> 'TenantCustomer':
        return cls(
            id=TenantCustomerId(verified_data.get('id', uuid.uuid4())),
            tenant_id=TenantId(verified_data.get('tenant_id')),
            user=User.from_payload(verified_data),
            status=TenantCustomerStatus.from_value(
                verified_data.get('status', str(TenantCustomerStatus.NEW))
            ),
            created_at=None,
            phone_number=(
                PhoneNumber.from_dict(verified_data.get('phone_number'))
                if validate_mandatory(verified_data, 'phone_number')
                else None
            ),
            email_address=(
                EmailAddress.from_dict(verified_data.get('email_address'))
                if validate_mandatory(verified_data, 'email_address')
                else None
            ),
            first_name=(verified_data.get('first_name') if 'first_name' in verified_data else None),
            paternal_surname=(
                verified_data.get('paternal_surname')
                if 'paternal_surname' in verified_data
                else None
            ),
            maternal_surname=(
                verified_data.get('maternal_surname')
                if 'maternal_surname' in verified_data
                else None
            ),
            photo=(
                verified_data.get('photo') if validate_mandatory(verified_data, 'photo') else None
            ),
            lang=(
                Language.from_value(verified_data.get('lang', Language.ES))
                if validate_mandatory(verified_data, 'lang')
                else None
            ),
            birth_date=(verified_data.get('birth_date') if 'birth_date' in verified_data else None),
            gender=(
                Gender.from_value(verified_data.get('gender'))
                if validate_mandatory(verified_data, 'gender')
                else None
            ),
            photo_url=None,
            creation_source=(
                TenantCustomerCreationSource.from_value(
                    verified_data.get('creation_source')
                ) if validate_mandatory(verified_data, 'creation_source') else None
            ),
        )

    def set_active(self):
        self.status = TenantCustomerStatus.ACTIVE

    def overload(
        self,
        new_instance: 'TenantCustomer',
        properties: List[str] = None,
    ):
        instance_properties = properties or [
            'user',
            'status',
            'email_address',
            'phone_number',
            'first_name',
            'paternal_surname',
            'maternal_surname',
            'birth_date',
            'lang',
            'photo',
            'gender',
            'qr_passcode',
            'access_code',
        ]
        for _property in instance_properties:
            if not hasattr(self, _property):
                continue
            property_value = getattr(new_instance, _property)
            setattr(self, _property, property_value)

    @property
    def to_persist_dict(self) -> dict:
        persist_data = {
            'user_id': self.user.id,
            'status': self.status,
            'creation_source': self.creation_source,
            'email_address_id': (str(self.email_address.id) if self.email_address else None),
            'phone_number_id': (str(self.phone_number.id) if self.phone_number else None),
            'first_name': self.first_name,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
            'birth_date': self.birth_date,
            'lang': self.lang,
            'gender': self.gender,
        }
        if self.photo:
            persist_data['photo'] = self.photo
        return persist_data

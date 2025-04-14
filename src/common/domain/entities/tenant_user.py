# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.common.constants import DEFAULT_LANGUAGE
from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.mixins.profile import DomainProfileMixin
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.user import User
from src.common.domain.entities.user_profile import UserProfile
from src.common.domain.value_objects import TenantCustomerId, TenantId, TenantUserId
from src.common.helpers.dicts import validate_mandatory


@dataclass
class TenantUser(DomainProfileMixin, AggregateRoot):
    id: TenantUserId
    tenant_id: TenantId
    user: User
    status: TenantUserStatus
    is_owner: bool = False
    created_at: Optional[datetime] = None

    def __eq__(self, other: 'TenantUser'):
        return self.id == other.id

    @property
    def email(self) -> str:
        return self.user.email_address.email

    @property
    def email_address(self) -> Optional[EmailAddress]:
        return self.user.email_address

    @property
    def phone_number(self) -> Optional[PhoneNumber]:
        return self.user.phone_number

    @property
    def is_email_reachable(self) -> bool:
        return self.user.is_email_reachable

    @property
    def is_phone_number_reachable(self) -> bool:
        return self.user.is_phone_number_reachable

    @property
    def is_reachable(self) -> bool:
        return self.is_email_reachable or self.is_phone_number_reachable

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
            birth_date=None,
            gender=None,
        )

    @property
    def channel_id(self) -> str:
        return f'TenantUser@{self.id}'

    @property
    def is_new(self) -> bool:
        return self.created_at is None

    @property
    def is_active(self) -> bool:
        return self.status == TenantUserStatus.ACTIVE

    @classmethod
    def from_payload(cls, verified_data) -> 'TenantUser':
        return cls(
            id=TenantCustomerId(verified_data.get('id', uuid.uuid4())),
            tenant_id=TenantId(verified_data.get('tenant_id')),
            user=User.from_payload(
                verified_data={'id': uuid.uuid4()},
                email_address=(
                    EmailAddress.from_dict(verified_data.get('email_address'))
                    if verified_data.get('email_address')
                    else None
                ),
                phone_number=(
                    PhoneNumber.from_dict(verified_data.get('phone_number'))
                    if verified_data.get('phone_number')
                    else None
                ),
            ),
            status=TenantUserStatus.from_value(
                verified_data.get('status', str(TenantUserStatus.PENDING))
            ),
            created_at=None,
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
            photo_url=None,
            birth_date=None,
            gender=None,
        )

    def activate(self):
        self.status = TenantUserStatus.ACTIVE

    def overload(
        self,
        new_instance: 'TenantUser',
        properties: List[str] = None,
    ):
        instance_properties = properties or [
            'status',
            'first_name',
            'paternal_surname',
            'maternal_surname',
            'status',
            'lang',
            'photo',
        ]

        user_properties = User.get_overload_properties()
        overload_user_properties = []
        for _property in instance_properties:
            if _property in user_properties:
                overload_user_properties.append(_property)
                continue
            if not hasattr(self, _property):
                continue
            property_value = getattr(new_instance, _property)
            setattr(self, _property, property_value)

        self.user.overload(
            new_instance=new_instance.user,
            properties=overload_user_properties,
        )

    @property
    def to_persist_dict(self) -> dict:
        persist_data = {
            'user_id': self.user.id,
            'status': self.status,
            'first_name': self.first_name,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
            'lang': self.lang,
        }
        if self.photo:
            persist_data['photo'] = self.photo
        return persist_data

    @classmethod
    def empty(cls, user: Optional[User] = None) -> 'TenantUser':
        empty_user = user or User.empty()
        return cls(
            id=TenantUserId(str(empty_user.id)),
            tenant_id=TenantId(str(empty_user.id)),
            user=empty_user,
            status=TenantUserStatus.PENDING,
            created_at=None,
            first_name=None,
            paternal_surname=None,
            maternal_surname=None,
            lang=DEFAULT_LANGUAGE,
            photo=None,
            photo_url=None,
            birth_date=None,
            gender=None,
            is_owner=False,
        )

# -*- coding: utf-8 -*-

from dataclasses import asdict, dataclass
from typing import Optional

from src.common.domain.enums.growth import TenantLeadChannel, TenantLeadStage
from src.common.domain.enums.users import TenantCustomerStatus, TenantUserStatus, TenantCustomerCreationSource
from src.common.domain.messaging.commands import Command
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.tenant_customer_lead import TenantCustomerLead
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.models.user import User
from src.common.domain.value_objects import TenantCustomerId, TenantId, UserId


@dataclass
class CreateBasicTenantCustomerCommand(Command):
    tenant_id: TenantId
    person: SimplePerson
    tenant_customer_id: Optional[TenantCustomerId] = None
    status: TenantCustomerStatus = TenantCustomerStatus.ACTIVE
    creation_source: Optional[TenantCustomerCreationSource] = None

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'CreateBasicTenantCustomerCommand':
        return cls(**kwargs)


@dataclass
class RegisterCustomerInTenantCommand(Command):
    tenant_id: TenantId
    user: User
    status: TenantCustomerStatus = TenantCustomerStatus.ACTIVE

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'RegisterCustomerInTenantCommand':
        return cls(**kwargs)


@dataclass
class RegisterUserInTenantCommand(Command):
    tenant_id: TenantId
    user: User
    status: TenantUserStatus = TenantUserStatus.ACTIVE
    is_owner: bool = False

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'RegisterUserInTenantCommand':
        return cls(**kwargs)


@dataclass
class RegisterUserCommand(Command):
    instance: User
    raw_password: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'RegisterUserCommand':
        return cls(**kwargs)


@dataclass
class SetUserPasswordCommand(Command):
    user_id: UserId
    new_password: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SetUserPasswordCommand':
        return cls(**kwargs)


@dataclass
class DeactivateUserCommand(Command):
    user_id: UserId

    @property
    def to_dict(self) -> dict:
        return {
            'user_id': str(self.user_id),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'DeactivateUserCommand':
        return cls(
            user_id=UserId(kwargs['user_id']),
        )


@dataclass
class PersistPhoneNumberCommand(Command):
    instance: PhoneNumber

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PersistPhoneNumberCommand':
        return cls(**kwargs)


@dataclass
class PersistEmailAddressCommand(Command):
    instance: EmailAddress

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PersistEmailAddressCommand':
        return cls(**kwargs)


@dataclass
class CreateTenantLeadCommand(Command):
    tenant_id: TenantId
    person: SimplePerson
    channel: TenantLeadChannel
    status: TenantLeadStage

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'CreateTenantLeadCommand':
        return cls(**kwargs)


@dataclass
class PersistTenantCustomerLeadCommand(Command):
    tenant_id: TenantId
    instance: TenantCustomerLead

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PersistTenantCustomerLeadCommand':
        return cls(**kwargs)


@dataclass
class PersistTenantCustomerCommand(Command):
    instance: TenantCustomer

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PersistTenantCustomerCommand':
        return cls(**kwargs)


@dataclass
class PersistTenantUserCommand(Command):
    instance: TenantUser

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'PersistTenantUserCommand':
        return cls(**kwargs)

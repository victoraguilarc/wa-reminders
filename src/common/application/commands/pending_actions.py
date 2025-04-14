from dataclasses import dataclass
from typing import Optional

from src.common.domain.enums.locales import Language
from src.common.domain.messaging.commands import Command
from src.common.domain.value_objects import TenantUserId, TenantId, TenantCustomerId


@dataclass
class SendWhatsappSessionRedemptionCommand(Command):
    phone_number: str
    tenant_name: str
    first_name: str
    action_link: str
    language: Language = Language.ES
    access_code_url: Optional[str] = None

    @property
    def to_dict(self) -> dict:
        return {
            'phone_number': self.phone_number,
            'tenant_name': self.tenant_name,
            'first_name': self.first_name,
            'action_link': self.action_link,
            'language': str(self.language),
            'access_code_url': self.access_code_url,
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendWhatsappSessionRedemptionCommand':
        return cls(
            phone_number=kwargs['phone_number'],
            tenant_name=kwargs['tenant_name'],
            first_name=kwargs['first_name'],
            action_link=kwargs['action_link'],
            language=Language.from_value(kwargs['language']),
            access_code_url=kwargs['access_code_url'],
        )


@dataclass
class SendEmailSessionRedemptionCommand(Command):
    email: str
    tenant_name: str
    first_name: str
    action_link: str
    access_code_url: Optional[str] = None

    @property
    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'tenant_name': self.tenant_name,
            'first_name': self.first_name,
            'action_link': self.action_link,
            'access_code_url': self.access_code_url,
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendEmailSessionRedemptionCommand':
        return cls(
            email=kwargs['email'],
            tenant_name=kwargs['tenant_name'],
            first_name=kwargs['first_name'],
            action_link=kwargs['action_link'],
            access_code_url=kwargs['access_code_url'],
        )


@dataclass
class RequestTenantUserInvitationCommand(Command):
    tenant_id: TenantId
    tenant_user_id: TenantUserId

    @property
    def to_dict(self) -> dict:
        return {
            'tenant_id': str(self.tenant_id),
            'tenant_user_id': str(self.tenant_user_id),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'RequestTenantUserInvitationCommand':
        return cls(
            tenant_id=TenantId(kwargs['tenant_id']),
            tenant_user_id=TenantUserId(kwargs['tenant_user_id']),
        )


@dataclass
class SendTenantCustomerAccessCodeCommand(Command):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId

    @property
    def to_dict(self) -> dict:
        return {
            'tenant_id': str(self.tenant_id),
            'tenant_customer_id': str(self.tenant_customer_id),
        }

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'SendTenantCustomerAccessCodeCommand':
        return cls(
            tenant_id=TenantId(kwargs['tenant_id']),
            tenant_customer_id=TenantCustomerId(kwargs['tenant_customer_id']),
        )

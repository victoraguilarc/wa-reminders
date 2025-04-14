# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.common.application.helpers.actions import get_action_valid_until
from src.common.constants import (
    DEFAULT_PENDING_ACTION_SESSION_USAGE_LIMIT,
    DEFAULT_PENDING_ACTION_USAGE_LIMIT,
    UNIQUE_USAGE_LIMIT,
)
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.value_objects import PendingActionId
from src.common.helpers.enconding import encode_base64
from src.pending_actions.domain.types.email_address_verification import EmailAddressVerification
from src.pending_actions.domain.types.phone_number_verification import PhoneNumberVerification
from src.pending_actions.domain.types.tenant_customer_session_redemption import (
    TenantCustomerSessionRedemption,
)
from src.pending_actions.domain.types.tenant_user_invitation import TenantUserInvitation
from src.pending_actions.domain.types.user_reset_password import UserResetPassword


@dataclass
class PendingAction(AggregateRoot):
    id: PendingActionId
    token: str
    tracking_code: str
    category: PendingActionCategory
    status: PendingActionStatus
    group_id: Optional[str] = None
    created_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    metadata: dict = None
    usage_limit: int = DEFAULT_PENDING_ACTION_USAGE_LIMIT
    usage: int = 0

    def __post_init__(self):
        self.metadata = self.metadata or {}

    @property
    def is_usage_limit_reached(self):
        return self.usage >= self.usage_limit

    @property
    def is_email_verification(self):
        return self.category == PendingActionCategory.EMAIL_ADDRESS_VERIFICATION

    @property
    def is_phone_verification(self):
        return self.category == PendingActionCategory.PHONE_NUMBER_VERIFICATION

    @property
    def is_tenant_customer_session_redemption(self):
        return self.category == PendingActionCategory.TENANT_CUSTOMER_SESSION_REDEMPTION

    @property
    def is_user_reset_password(self):
        return self.category == PendingActionCategory.USER_RESET_PASSWORD

    @property
    def is_tenant_user_invitation(self):
        return self.category == PendingActionCategory.TENANT_USER_INVITATION

    @property
    def is_expired(self):
        return self.status == PendingActionStatus.EXPIRED

    @property
    def is_completed(self) -> bool:
        return self.status == PendingActionStatus.COMPLETED

    @property
    def is_pending(self) -> bool:
        return self.status == PendingActionStatus.PENDING

    @property
    def is_actionable(self) -> bool:
        return (
            self.status == PendingActionStatus.PENDING
            and self.usage < self.usage_limit
        )

    @property
    def to_tracking_dict(self):
        return {
            'tracking_code': str(self.tracking_code),
            'category': str(self.category),
            'status': str(self.status),
        }

    @property
    def to_persist_dict(self):
        return {
            'group_id': self.group_id,
            'token': self.token,
            'tracking_code': self.tracking_code,
            'category': str(self.category),
            'status': str(self.status),
            'completed_at': self.completed_at,
            'expired_at': self.expired_at,
            'valid_until': self.valid_until,
            'metadata': self.metadata,
            'usage': self.usage,
            'usage_limit': self.usage_limit,
        }

    @property
    def channel_id(self):
        return f'PendingAction@{self.tracking_code}'

    def is_in_metadata(self, key: str) -> bool:
        return key in self.metadata

    def complete(self):
        self.status = PendingActionStatus.COMPLETED

    def cancel(self):
        self.status = PendingActionStatus.EXPIRED

    def increment_usage(self):
        self.usage += 1

    @classmethod
    def email_address_verification(
        cls,
        group_id: str,
        metadata: EmailAddressVerification,
    ) -> 'PendingAction':
        return PendingAction(
            id=PendingActionId(uuid.uuid4()),
            token=encode_base64(uuid.uuid4().hex),
            tracking_code=str(uuid.uuid4().hex),
            group_id=group_id,
            category=PendingActionCategory.EMAIL_ADDRESS_VERIFICATION,
            status=PendingActionStatus.PENDING,
            valid_until=get_action_valid_until(),
            metadata=metadata.to_dict,
            usage_limit=UNIQUE_USAGE_LIMIT,
        )

    @classmethod
    def phone_number_verification(
        cls,
        group_id: str,
        metadata: PhoneNumberVerification,
    ) -> 'PendingAction':
        return PendingAction(
            id=PendingActionId(uuid.uuid4()),
            token=encode_base64(uuid.uuid4().hex),
            tracking_code=str(uuid.uuid4().hex),
            group_id=group_id,
            category=PendingActionCategory.PHONE_NUMBER_VERIFICATION,
            status=PendingActionStatus.PENDING,
            valid_until=get_action_valid_until(),
            metadata=metadata.to_dict,
        )

    @classmethod
    def tenant_customer_session_redemption(
        cls,
        group_id: str,
        metadata: TenantCustomerSessionRedemption,
    ) -> 'PendingAction':
        return PendingAction(
            id=PendingActionId(uuid.uuid4()),
            token=encode_base64(uuid.uuid4().hex),
            tracking_code=uuid.uuid4().hex,
            group_id=group_id,
            category=PendingActionCategory.TENANT_CUSTOMER_SESSION_REDEMPTION,
            status=PendingActionStatus.PENDING,
            valid_until=get_action_valid_until(),
            metadata=metadata.to_dict,
            usage_limit=DEFAULT_PENDING_ACTION_SESSION_USAGE_LIMIT,
        )

    @classmethod
    def tenant_user_invitation(
        cls,
        group_id: str,
        metadata: TenantUserInvitation,
    ) -> 'PendingAction':
        return PendingAction(
            id=PendingActionId(uuid.uuid4()),
            token=encode_base64(uuid.uuid4().hex),
            tracking_code=uuid.uuid4().hex,
            group_id=group_id,
            category=PendingActionCategory.TENANT_USER_INVITATION,
            status=PendingActionStatus.PENDING,
            valid_until=get_action_valid_until(),
            metadata=metadata.to_dict,
            usage_limit=UNIQUE_USAGE_LIMIT,
        )

    @classmethod
    def user_reset_password(
        cls,
        group_id: str,
        metadata: UserResetPassword,
    ) -> 'PendingAction':
        return PendingAction(
            id=PendingActionId(uuid.uuid4()),
            token=encode_base64(uuid.uuid4().hex),
            tracking_code=uuid.uuid4().hex,
            group_id=group_id,
            category=PendingActionCategory.USER_RESET_PASSWORD,
            status=PendingActionStatus.PENDING,
            valid_until=get_action_valid_until(),
            metadata=metadata.to_dict,
            usage_limit=UNIQUE_USAGE_LIMIT,
        )

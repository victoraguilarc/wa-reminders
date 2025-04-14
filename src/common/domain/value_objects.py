# -*- coding: utf-8 -*-

import tempfile
from dataclasses import dataclass
from typing import NewType, Optional, Type, Union
from uuid import UUID

from src.common.domain.enums.countries import CountryIsoCode


@dataclass
class RawPhoneNumber:
    dial_code: int
    phone_number: str
    iso_code: Optional[CountryIsoCode]
    prefix: Optional[str]

    @property
    def display_phone(self) -> str:
        return f'+{self.dial_code}{self.phone_number}'

    @property
    def formatted_phone_number(self) -> str:
        return f'+{self.dial_code} {self.phone_number}'

    @property
    def international_number(self) -> str:
        if self.prefix:
            return f'{self.dial_code}{self.prefix}{self.phone_number}'
        return f'{self.dial_code}{self.phone_number}'

    @property
    def to_persist_dict(self):
        return {
            'iso_code': str(self.iso_code),
            'prefix': self.prefix,
        }

    @property
    def to_dict(self):
        return {
            'iso_code': str(self.iso_code),
            'dial_code': self.dial_code,
            'phone_number': self.phone_number,
            'prefix': self.prefix,
        }


    @classmethod
    def from_dict(cls, instance_data: dict) -> 'RawPhoneNumber':
        return RawPhoneNumber(
            iso_code=CountryIsoCode.from_value(instance_data.get('iso_code')),
            dial_code=int(instance_data.get('dial_code')),
            phone_number=str(instance_data.get('phone_number')),
            prefix=instance_data.get('prefix'),
        )


class Slug(str):
    def validate(self):
        raise NotImplemented


UserId = NewType('UserId', Union[UUID, str])
UserSessionToken = NewType('UserSessionToken', dict)

TenantId = NewType('TenantId', Union[UUID, int])
TenantUserId = NewType('TenantUserId', Union[UUID, int])
TenantCustomerId = NewType('TenantCustomerId', Union[UUID, int])
TenantCustomerLeadId = NewType('TenantCustomerLeadId', Union[UUID, int])
TenantCustomerLeadAttemptId = NewType('TenantCustomerLeadAttemptId', Union[UUID, int])
TenantRoleId = NewType('TenantRoleId', Union[UUID, int])
TenantWhatsappSessionId = NewType('TenantWhatsappSessionId"', Union[UUID, int])
TenantBranchId = NewType('TenantBranchId', Union[UUID, int])

EmailAddressId = NewType('EmailAddressId', Union[UUID, str])
PhoneNumberId = NewType('PhoneNumberId', Union[UUID, int])
PendingActionId = NewType('PendingActionId', Union[UUID, int])

CountryId = NewType('CountryId', Union[UUID, str])
StateId = NewType('StateId', Union[UUID, str])
CityId = NewType('CityId', Union[UUID, str])
TownHallId = NewType('TownHallId', Union[UUID, str])
AddressId = NewType('AddressId', Union[UUID, str])

TenantClassId = NewType('TenantClassId', Union[UUID, int])
TenantClassPassId = NewType('TenantClassPassId', Union[UUID, int])
TenantClassSessionId = NewType('TenantClassSessionId', Union[UUID, int])
TenantClassSessionAttendeeId = NewType('TenantClassSessionAttendeeId', Union[UUID, int])
TenantClassSessionPassId = NewType('TenantClassSessionPassId', Union[UUID, int])
TenantClassScheduleId = NewType('TenantClassScheduleId', Union[UUID, int])
TenantBatchId = NewType('TenantBatchId', Union[UUID, int])
TenantClassBatchId = NewType('TenantClassBatchId', Union[UUID, int])
TenantPictureId = NewType('TenantPictureId', Union[UUID, int])
TenantResourceId = NewType('TenantResourceId', Union[UUID, int])

AccessCodeId = NewType('AccessCodeId', Union[UUID, int])
PictureId = NewType('PictureId', Union[UUID, int])
DocumentId = NewType('PictureId', Union[UUID, int])
PlaceId: Type[UUID | int] = NewType('PlaceId', Union[UUID, int])
LinkedSiteId = NewType('LinkedSiteId', Union[UUID, int])
ContactMessageId = NewType('ContactMessageId', Union[UUID, int])

PaymentRequestId = NewType('PaymentRequestId', Union[UUID, int])
PaymentRecordId = NewType('PaymentRecordId', Union[UUID, int])

NotificationId = NewType('NotificationId', Union[UUID, int])
NotificationTemplateId = NewType('NotificationTemplateId', Union[UUID, int])

PaymentMethodId = NewType('PaymentMethodId', Union[UUID, str, int])
PaymentIntentId = NewType('PaymentIntentId', Union[UUID, str, int])
PaymentSubscriptionId = NewType('PaymentSubscriptionId', Union[UUID, str, int])
PaymentSubscriptionItemId = NewType('PaymentSubscriptionItemId', Union[UUID, str, int])
PaymentAccountId = NewType('PaymentAccountId', Union[UUID, str, int])
PaymentCustomerId = NewType('PaymentCustomerId', Union[UUID, str, int])
PaymentPriceId = NewType('PaymentPriceId', Union[UUID, str, int])
PaymentProductId = NewType('PaymentProductId', Union[UUID, str, int])

ProviderPaymentIntentId = NewType('ProviderPaymentIntentId', Union[UUID, str, int])
ProviderPaymentCustomerId = NewType('ProviderPaymentCustomerId', Union[UUID, str, int])
ProviderPaymentAccountId = NewType('ProviderPaymentAccountId', Union[UUID, str, int])
ProviderPaymentPriceId = NewType('ProviderPaymentPriceId', Union[UUID, str, int])
ProviderPaymentProductId = NewType('ProviderPaymentProductId', Union[UUID, str, int])
ProviderPaymentSubscriptionId = NewType('ProviderPaymentSubscriptionId', Union[UUID, str, int])
ProviderPaymentSubscriptionItemId = NewType(
    'ProviderPaymentSubscriptionItemId', Union[UUID, str, int]
)

TierId = NewType('TierId', Union[UUID, str, int])
TenantTierId = NewType('TenantTierId', Union[UUID, str, int])

TenantCourseId = NewType('TenantCourseId', Union[UUID, str, int])
TenantCourseChapterId = NewType('TenantCourseChapterId', Union[UUID, str, int])
TenantCourseLessonId = NewType('TenantCourseLessonId', Union[UUID, str, int])
TenantVideoId = NewType('TenantVideoId', Union[UUID, str, int])

MembershipId = NewType('MembershipId', Union[UUID, str, int])
MembershipPlanId = NewType('MembershipPlanId', Union[UUID, str, int])
MembershipChangeId = NewType('MembershipChangeId', Union[UUID, str, int])
MembershipChangeItemId: Type[UUID | int] = NewType('MembershipChangeItemId', Union[UUID, str, int])
MembershipPurchaseId = NewType('MembershipPurchaseId', Union[UUID, str, int])
MembershipPurchaseItemId: Type[UUID | int] = NewType(
    'MembershipPurchaseItemId', Union[UUID, str, int]
)
MembershipRechargeId = NewType('MembershipRechargeId', Union[UUID, str, int])
MembershipEventId = NewType('MembershipEventId', Union[UUID, str, int])


class TenantSlug(Slug):
    pass


@dataclass
class RawPicture(object):
    image: tempfile

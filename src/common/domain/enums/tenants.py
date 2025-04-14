# -*- coding: utf-8 -*-

from src.common.domain import BaseEnum


class TenantStatus(BaseEnum):
    ACTIVE = 'ACTIVE'
    PENDING = 'PENDING'
    INACTIVE = 'INACTIVE'
    SUSPENDED = 'SUSPENDED'


class TenantClassLevel(BaseEnum):
    BASIC = 'BASIC'
    INTERMEDIATE = 'INTERMEDIATE'
    ADVANCED = 'ADVANCED'

    @classmethod
    def choices(cls):  # noqa: D102
        return (
            (cls.BASIC.value, 'BASIC'),
            (cls.INTERMEDIATE.value, 'INTERMEDIATE'),
            (cls.ADVANCED.value, 'ADVANCED'),
        )


class TenantBatchStatus(BaseEnum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ARCHIVED = 'ARCHIVED'


class TenantPictureCategory(BaseEnum):
    AVATAR = 'AVATAR'
    CLASS = 'CLASS'
    BADGE = 'BADGE'
    GENERAL = 'GENERAL'
    QR_CODE = 'QR_CODE'

    @classmethod
    def choices(cls):  # noqa: D102
        return (
            (cls.AVATAR.value, 'AVATAR'),
            (cls.CLASS.value, 'CLASS'),
            (cls.BADGE.value, 'BADGE'),
            (cls.GENERAL.value, 'GENERAL'),
            (cls.QR_CODE.value, 'QR_CODE'),
        )


class TenantTierStatus(BaseEnum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class LinkedSiteCategory(BaseEnum):
    MEMBERS_SITE = 'MEMBERS_SITE'

    @property
    def is_members_site(self):
        return self == self.MEMBERS_SITE


class TenantResourceCategory(BaseEnum):
    VIDEO = 'VIDEO'
    IMAGE = 'IMAGE'
    LINK = 'LINK'
    LOCATION = 'LOCATION'
    TESTIMONIAL = 'TESTIMONIAL'
    SOCIAL_MEDIA = 'SOCIAL_MEDIA'
    MESSAGE = 'MESSAGE'



class WhatsappSessionStatus(BaseEnum):
    STARTING = 'STARTING'
    STOPPED = 'STOPPED'
    SCAN_QR_CODE = 'SCAN_QR_CODE'
    FAILED = 'FAILED'
    WORKING = 'WORKING'

    @property
    def is_starting(self) -> bool:
        return self == self.STARTING

    @property
    def is_stopped(self) -> bool:
        return self == self.STOPPED

    @property
    def is_scan_qr_code(self) -> bool:
        return self == self.SCAN_QR_CODE

    @property
    def is_failed(self) -> bool:
        return self == self.FAILED

    @property
    def is_working(self) -> bool:
        return self == self.WORKING

    @classmethod
    def refresh_statuses(cls):
        return [
            cls.SCAN_QR_CODE,
            cls.STOPPED,
            cls.FAILED,
            cls.WORKING,
        ]


from src.common.domain import BaseEnum


class PendingActionCategory(BaseEnum):
    USER_RESET_PASSWORD = 'USER_RESET_PASSWORD'
    EMAIL_ADDRESS_VERIFICATION = 'EMAIL_ADDRESS_VERIFICATION'
    PHONE_NUMBER_VERIFICATION = 'PHONE_NUMBER_VERIFICATION'
    TENANT_CUSTOMER_SESSION_REDEMPTION = 'TENANT_CUSTOMER_SESSION_REDEMPTION'
    TENANT_USER_INVITATION = 'TENANT_USER_INVITATION'

    @classmethod
    def get_verifications(cls):
        return [
            cls.EMAIL_ADDRESS_VERIFICATION,
            cls.PHONE_NUMBER_VERIFICATION,
        ]


class PendingActionStatus(BaseEnum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'


class Gender(BaseEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class TenantCustomerStatus(BaseEnum):
    NEW = 'NEW'
    LEAD = 'LEAD'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    CANCELLED = 'CANCELLED'

    @property
    def is_new(self) -> bool:
        return self == self.NEW

    @property
    def is_lead(self) -> bool:
        return self == self.LEAD

    @property
    def is_active(self) -> bool:
        return self == self.ACTIVE

    @property
    def is_inactive(self) -> bool:
        return self == self.INACTIVE

    @property
    def is_cancelled(self) -> bool:
        return self == self.CANCELLED


class TenantCustomerCreationSource(BaseEnum):
    UNDEFINED = 'UNDEFINED'
    TENANT_PAGE = 'TENANT_PAGE'
    MOBILE_ADMIN = 'MOBILE_ADMIN'
    WEB_ADMIN = 'WEB_ADMIN'
    WHATSAPP = 'WHATSAPP'


class TenantUserStatus(BaseEnum):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


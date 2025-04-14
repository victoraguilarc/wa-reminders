from src.common.domain import BaseEnum


class UserEvent(BaseEnum):
    EMAIL_VERIFIED = 'User.EmailVerified'


class TenantCustomerEvent(BaseEnum):
    UPDATED = 'TenantCustomer.Updated'
    MEMBERSHIP_UPDATED = 'TenantCustomer.MembershipUpdated'


class PendingActionEvent(BaseEnum):
    UPDATED = 'PendingAction.Updated'


class PaymentIntentEvent(BaseEnum):
    UPDATED = 'PaymentIntent.Updated'


class WhatsappSessionEvent(BaseEnum):
    STATUS_UPDATED = 'WhatsappSession.StatusUpdated'
    REFRESH_SESSIONS = 'WhatsappSession.RefreshSessions'

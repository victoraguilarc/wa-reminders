from src.common.domain.exceptions.common import NotFound


class MembershipPlanNotFound(NotFound):
    pass


class MembershipNotFoundError(NotFound):
    pass


class InvalidMembershipError(NotFound):
    pass


class ExpiredMembershipError(NotFound):
    pass


class InactiveMembershipError(NotFound):
    pass


class InsufficientPassesBalanceError(NotFound):
    pass


class MembershipPurchaseNotFound(NotFound):
    pass


class MembershipRechargeNotFound(NotFound):
    pass


class MembershipChangeNotFound(NotFound):
    pass


class MembershipPurchaseFromPaymentNotFound(NotFound):
    pass


class MembershipRechargeFromPaymentNotFound(NotFound):
    pass


class MembershipChangeFromPaymentNotFound(NotFound):
    pass

from src.common.domain.exceptions.common import Forbidden, NotFound


class InvalidPasswordError(NotFound):
    pass

class SamePasswordsError(NotFound):
    pass

class UserNotFoundError(NotFound):
    pass


class NotEnoughTenantPermissions(Forbidden):
    pass

class TenantUserNotFoundError(NotFound):
    pass

class TenantCustomerNotFoundError(NotFound):
    pass

class TenantCustomerNotReachableError(NotFound):
    pass

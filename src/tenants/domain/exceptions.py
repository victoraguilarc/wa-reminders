from src.common.domain.exceptions.common import BadRequest, NotFound, UntrackedError


class TenantNotFoundError(NotFound, UntrackedError):
    pass


class TenantPictureNotFoundError(NotFound):
    pass


class TenantLimitExcedeedError(BadRequest):
    pass


class TenantBranchNotFoundError(BadRequest):
    pass

class TenantWhatsappSessionNotFoundError(BadRequest):
    pass


class TenantWhatsappUnavailableQRCodeError(BadRequest):
    pass


class TenantWhatsappSessionsLimitReachedError(BadRequest):
    pass


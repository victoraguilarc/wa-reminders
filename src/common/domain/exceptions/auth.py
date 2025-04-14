from src.common.domain.exceptions.common import NotFound


class EmailAddressNotFoundError(NotFound):
    pass


class PhoneNumberNotFoundError(NotFound):
    pass


class EmailAddressIsAlreadyVerifiedError(NotFound):
    pass


class PhoneNumberIsAlreadyVerifiedError(NotFound):
    pass

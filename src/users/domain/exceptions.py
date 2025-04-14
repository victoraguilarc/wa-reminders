# -*- coding: utf-8 -*-

from src.common.domain.exceptions.common import BadRequest, NotFound


class TenantCustomerLeadNotFoundError(NotFound):
    pass

class PhoneNumberIsAlreadyUsedError(BadRequest):
    pass


class TenantCustomerWithoutEmailAddressError(BadRequest):
    pass


class TenantCustomerEmailIsAlreadyVerifiedError(BadRequest):
    pass


class TenantCustomerWithoutPhoneNumberError(BadRequest):
    pass


class TenantCustomerPhoneIsAlreadyVerifiedError(BadRequest):
    pass


class TenantUserMustHaveAtLeastOneAuthMethodError(BadRequest):
    pass

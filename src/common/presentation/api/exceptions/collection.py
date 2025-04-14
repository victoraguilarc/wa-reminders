# -*- coding: utf-8 -*-
import logging
from typing import Type

from django.utils.translation import gettext_lazy as _

from src.auth.domain.exceptions import (
    InvalidCredentials,
    InvalidCredentialsForTenant,
    PictureNotFound,
)
from src.common.domain.exceptions.auth import (
    EmailAddressIsAlreadyVerifiedError,
    PhoneNumberIsAlreadyVerifiedError,
)
from src.common.domain.exceptions.common import (
    DomainEmptyPage,
    DomainException,
    EmailIsAlreadyUsedError,
    UnAuthenticated,
)
from src.common.domain.exceptions.users import (
    NotEnoughTenantPermissions,
    UserNotFoundError,
    InvalidPasswordError,
    SamePasswordsError,
    TenantUserNotFoundError,
    TenantCustomerNotFoundError,
    TenantCustomerNotReachableError,
)
from src.common.presentation.api.exceptions.base import (
    APIBadRequest,
    APIBaseException,
    APINotAuthenticated,
    APINotFound,
    APINotImplemented,
    APIPermissionDenied,
    APIUnauthorized,
    GenericError,
)
from src.pending_actions.domain.exceptions import (
    InvalidPendingActionError,
    PendingActionNotFoundError,
)
from src.tenants.domain.exceptions import (
    TenantLimitExcedeedError,
    TenantNotFoundError,
    TenantPictureNotFoundError,
    TenantWhatsappSessionsLimitReachedError,
    TenantWhatsappSessionNotFoundError,
    TenantWhatsappUnavailableQRCodeError,
)
from src.users.domain.exceptions import (
    PhoneNumberIsAlreadyUsedError,
    TenantCustomerEmailIsAlreadyVerifiedError,
    TenantCustomerPhoneIsAlreadyVerifiedError,
    TenantCustomerWithoutEmailAddressError,
    TenantCustomerWithoutPhoneNumberError,
    TenantCustomerLeadNotFoundError,
    TenantUserMustHaveAtLeastOneAuthMethodError,
)

GENERIC_ERROR = GenericError(
    code='server_error',
    detail=_('Server Error'),
)

NOT_AUTHENTICATED = APINotAuthenticated(
    code='not_authenticated',
    detail=_('Authentication credentials were not provided.'),
)
INVALID_TOKEN = APINotAuthenticated(
    code='users.InvalidToken',
    detail=_('Invalid or Expired token'),
)
AUTHENTICATION_FAILED = APIUnauthorized(
    code='users.AuthenticationFailed',
    detail=_('Authentication Fails'),
)
TENANT_NOT_FOUND = APINotImplemented(
    code='common.TenantNotFound',
    detail=_('Tenant Not Found'),
)
TENANT_USER_NOT_FOUND = APINotFound(
    code='common.TenantUserNotFound',
    detail=_('Tenant User Not Found'),
)
TENANT_CUSTOMER_NOT_FOUND = APINotFound(
    code='common.TenantCustomerNotFound',
    detail=_('Tenant Customer Not Found'),
)
USER_NOT_FOUND = APINotFound(
    code='common.UserNotFound',
    detail=_('User Not Found'),
)
TENANT_ACCESS_UNAUTHORIZED = APIUnauthorized(
    code='common.TenantAccessUnauthorized',
    detail=_('Tenant Access Unauthorized'),
)
TENANT_ACTION_FORBIDDEN = APIPermissionDenied(
    code='common.TenantActionForbidden',
    detail=_('Has no enough permissions to perform this action'),
)
EMPTY_PAGE = APIBadRequest(
    code='common.EmptyPage',
    detail=_('There are no more items'),
)

error_codes = {
    UserNotFoundError: USER_NOT_FOUND,
    NotEnoughTenantPermissions: TENANT_ACTION_FORBIDDEN,
    DomainEmptyPage: EMPTY_PAGE,
    InvalidCredentials: APIUnauthorized(
        code='accounts.InvalidCredentials',
        detail=_('Invalid Credentials'),
    ),
    InvalidCredentialsForTenant: APIUnauthorized(
        code='accounts.InvalidCredentialsForTenant',
        detail=_('Invalid Credentials for Tenant'),
    ),
    PictureNotFound: APINotFound(
        code='common.PictureNotFound',
        detail=_('Picture Not Found'),
    ),
    UnAuthenticated: NOT_AUTHENTICATED,
    TenantNotFoundError: APINotFound(
        code='tenants.TenantNotFound',
        detail=_('Tenant Not Found'),
    ),
    TenantPictureNotFoundError: APINotFound(
        code='tenants.TenantPictureNotFound',
        detail=_('Tenant Picture Not Found'),
    ),
    TenantLimitExcedeedError: APIPermissionDenied(
        code='tenants.TenantLimitExcedeed',
        detail=_('Tenant limit excedeed'),
    ),
    TenantCustomerNotFoundError: APINotFound(
        code='tenants.TenantCustomerNotFound',
        detail=_('Tenant Customer not found'),
    ),
    TenantCustomerNotReachableError: APINotFound(
        code='tenants.TenantCustomerNotReachable',
        detail=_('Tenant Customer is not reachable'),
    ),
    TenantCustomerLeadNotFoundError: APINotFound(
        code='tenants.TenantCustomerLeadNotFound',
        detail=_('Tenant Customer Lead not found'),
    ),
    TenantUserNotFoundError: APINotFound(
        code='tenants.TenantUserNotFound',
        detail=_('Tenant User not found'),
    ),
    TenantWhatsappSessionNotFoundError: APINotFound(
        code='tenants.WhatsappSessionNotFound',
        detail=_('Whatsapp Session not found'),
    ),
    TenantWhatsappSessionsLimitReachedError: APIBadRequest(
        code='tenants.WhatsappSessionsLimitReached',
        detail=_('Whatsapp Sessions limit reached'),
    ),
    TenantWhatsappUnavailableQRCodeError: APIBadRequest(
        code='tenants.WhatsappUnavailableQRCode',
        detail=_('Whatsapp QR Code is unavailable'),
    ),
    InvalidPasswordError: APIBadRequest(
        code='users.InvalidPassword',
        detail=_('Invalid Password'),
    ),
    SamePasswordsError: APIBadRequest(
        code='users.SamePasswordsError',
        detail=_('The new password must be different from the current password'),
    ),
    EmailIsAlreadyUsedError: APIBadRequest(
        code='users.EmailIsAlreadyUsed',
        detail=_('This email is already being used'),
    ),
    EmailAddressIsAlreadyVerifiedError: APIBadRequest(
        code='users.EmailAddressIsAlreadyVerified',
        detail=_('This email is already verified'),
    ),
    PhoneNumberIsAlreadyUsedError: APIBadRequest(
        code='users.PhoneNumberIsAlreadyUsed',
        detail=_('This phone number is already being used'),
    ),
    PhoneNumberIsAlreadyVerifiedError: APIBadRequest(
        code='users.PhoneNumberIsAlreadyVerified',
        detail=_('This phone number is already verified'),
    ),
    TenantUserMustHaveAtLeastOneAuthMethodError : APIBadRequest(
        code='users.TenantUserMustHaveAtLeastOneAuthMethod',
        detail=_('User must have at least one auth method'),
    ),
    TenantCustomerWithoutEmailAddressError: APIBadRequest(
        code='users.TenantCustomerWithoutEmailAddress',
        detail=_('Customer has no email address'),
    ),
    TenantCustomerEmailIsAlreadyVerifiedError: APIBadRequest(
        code='users.TenantCustomerEmailIsAlreadyVerified',
        detail=_('Customer\'s email is already verified'),
    ),
    TenantCustomerWithoutPhoneNumberError: APIBadRequest(
        code='users.TenantCustomerWithoutPhoneNumber',
        detail=_('Customer has no phone number'),
    ),
    TenantCustomerPhoneIsAlreadyVerifiedError: APIBadRequest(
        code='users.TenantCustomerPhoneIsAlreadyVerified',
        detail=_('Customer\'s phone number is already verified'),
    ),
    PendingActionNotFoundError: APINotFound(
        code='pendingActions.PendingActionNotFound',
        detail=_('Pending Action not found'),
    ),
    InvalidPendingActionError: APIBadRequest(
        code='pendingActions.InvalidPendingToken',
        detail=_('the provided token is invalid'),
    ),
}


def get_error_code(error_class: Type[DomainException]) -> APIBaseException:
    error_instance = error_codes.get(error_class)
    if not error_instance:
        logging.error(error_class)
    return error_instance or GENERIC_ERROR

# -*- coding: utf-8 -*-

from django.urls import path

from src.pending_actions.presentation.api.email_address.verification_perform import (
    EmailAddressVerificationPerformView,
)
from src.pending_actions.presentation.api.email_address.verification_request import (
    EmailAddressVerificationRequestView,
)
from src.pending_actions.presentation.api.pending_action import PendingActionView
from src.pending_actions.presentation.api.phone_number.verification_perform import (
    PhoneNumberVerificationPerformView,
)
from src.pending_actions.presentation.api.phone_number.verification_request import (
    PhoneNumberVerificationRequestView,
)
from src.pending_actions.presentation.api.tenant_customer.email_verification_request import \
    TenantCustomerEmailAddressVerificationRequestView
from src.pending_actions.presentation.api.tenant_customer.phone_verification_request import \
    TenantCustomerPhoneNumberVerificationRequestView
from src.pending_actions.presentation.api.tenant_customer.send_access_code import TenantCustomerSendAccessCodeView
from src.pending_actions.presentation.api.tenant_customer.session_redemption_perform import (
    TenantCustomerSessionRedemptionPerformView,
)
from src.pending_actions.presentation.api.tenant_customer.session_redemption_request import \
    TenantCustomerSessionRedemptionRequestView, TenantCustomerSessionRedemptionRequestByIdView
from src.pending_actions.presentation.api.tenant_user.invitation_perform import TenantUserInvitationPerformView
from src.pending_actions.presentation.api.tenant_user.invitation_request import TenantUserInvitationRequestView, \
    TenantUserInvitationRequestByIdView
from src.pending_actions.presentation.api.tenant_user.reset_password_request import (
    TenantUserResetPasswordRequestByIdView,
)
from src.pending_actions.presentation.api.user.reset_password_perform import (
    UserResetPasswordPerformView,
)
from src.pending_actions.presentation.api.user.reset_password_request import UserResetPasswordRequestView
from src.pending_actions.presentation.views.stream import PendingActionStream

app_name = 'pending_actions'
urlpatterns = [
    # ~ P E N D I N G   A C T I O N S

    path(
        'actions/<str:token_or_tracking_code>/',
        PendingActionView.as_view(),
        name='pending-action',
    ),

    # ~ STREAMS
    path(
        'actions/<str:tracking_code>/stream/',
        view=PendingActionStream.as_view(),
        name='pending-action-stream',
    ),

    #  ~ E M A I L   A D D R E S S

    path(
        'actions/email-addresses/verification/',
        EmailAddressVerificationRequestView.as_view(),
        name='email-verification-request',
    ),
    path(
        'actions/email-addresses/verification/perform/',
        EmailAddressVerificationPerformView.as_view(),
        name='email-verification-perform',
    ),

    # ~ P H O N E   N U M B E R S

    path(
        'actions/phone-numbers/verification/',
        PhoneNumberVerificationRequestView.as_view(),
        name='phone-verification-request',
    ),
    path(
        'actions/phone-numbers/verification/perform/',
        PhoneNumberVerificationPerformView.as_view(),
        name='phone-verification-perform',
    ),

    # ~ U S E R S

    path(
        'actions/users/reset-password/',
        UserResetPasswordRequestView.as_view(),
        name='user-reset-password-request',
    ),
    path(
        'actions/users/reset-password/perform/',
        UserResetPasswordPerformView.as_view(),
        name='user-reset-password-perform',
    ),

    # ~ T E N A N T   U S E R S

    path(
        'actions/tenant-users/<uuid:tenant_user_id>/reset-password/',
        TenantUserResetPasswordRequestByIdView.as_view(),
        name='tenant-user-reset-password-request-id',
    ),
    path(
        'actions/tenant-users/invitation/',
        TenantUserInvitationRequestView.as_view(),
        name='tenant-user-invitation-request',
    ),
    path(
        'actions/tenant-users/<uuid:tenant_user_id>/invitation/',
        TenantUserInvitationRequestByIdView.as_view(),
        name='tenant-user-invitation-request-id',
    ),
    path(
        'actions/tenant-users/invitation/perform/',
        TenantUserInvitationPerformView.as_view(),
        name='tenant-user-invitation-perform',
    ),

    # ~ T E N A N T   C U S T O M E R S

    path(
        'actions/tenant-customers/<uuid:tenant_customer_id>/email-verification/',
        view=TenantCustomerEmailAddressVerificationRequestView.as_view(),
        name='tenant-customer-email-verification-request-id',
    ),
    path(
        'actions/tenant-customers/<uuid:tenant_customer_id>/phone-verification/',
        view=TenantCustomerPhoneNumberVerificationRequestView.as_view(),
        name='tenant-customer-phone-verification-request-id',
    ),
    path(
        'actions/tenant-customers/session-redemption/',
        view=TenantCustomerSessionRedemptionRequestView.as_view(),
        name='tenant-customer-session-redemption-request',
    ),
    path(
        'actions/tenant-customers/<uuid:tenant_customer_id>/session-redemption/',
        view=TenantCustomerSessionRedemptionRequestByIdView.as_view(),
        name='tenant-customer-session-redemption-request-id',
    ),
    path(
        'actions/tenant-customers/<uuid:tenant_customer_id>/access-code/',
        view=TenantCustomerSendAccessCodeView.as_view(),
        name='tenant-customer-access-code',
    ),
    path(
        'actions/tenant-customers/session-redemption/perform/',
        view=TenantCustomerSessionRedemptionPerformView.as_view(),
        name='tenant-customer-session-redemption-perform',
    ),


]

# -*- coding: utf-8 -*-

from django.urls import path

from src.pending_actions.presentation.views.email_address.verification import (
    EmailAddressVerificationView,
)
from src.pending_actions.presentation.views.phone_number.verification import (
    PhoneNumberVerificationView,
)
from src.pending_actions.presentation.views.tenant_customer.session_redemption import (
    TenantCustomerSessionRedemptionView,
)
from src.pending_actions.presentation.views.tenant_user.invitation import (
    TenantUserInvitationView,
)
from src.pending_actions.presentation.views.user.reset_password import (
    UserResetPasswordView,
)

app_name = 'pending_actions'
urlpatterns = [
    path(
        'email-addresses/verification/<str:token>/',
        EmailAddressVerificationView.as_view(),
        name='email-address-verification',
    ),
    path(
        'phone-numbers/verification/<str:token>/',
        view=PhoneNumberVerificationView.as_view(),
        name='phone-number-verification',
    ),
    path(
        'users/reset-password/<str:token>/',
        view=UserResetPasswordView.as_view(),
        name='user-reset-password',
    ),
    path(
        'tenant-users/invitation/<str:token>/',
        view=TenantUserInvitationView.as_view(),
        name='tenant-user-invitation',
    ),
    path(
        'tenant-customers/session-redemption/<str:token>/',
        view=TenantCustomerSessionRedemptionView.as_view(),
        name='tenant-customer-session-redemption',
    ),
]

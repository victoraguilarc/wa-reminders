# -*- coding: utf-8 -*-

from django.urls import path

from src.users.presentation.api.tenant_customer import TenantCustomerView
from src.users.presentation.api.tenant_customer_profile import TenantCustomerProfileView
from src.users.presentation.api.tenant_customers import TenantCustomersView
from src.users.presentation.api.tenant_user import TenantUserView
from src.users.presentation.api.tenant_user_password import TenantUserPasswordView
from src.users.presentation.api.tenant_user_profile import TenantUserProfileView
from src.users.presentation.api.tenant_users import TenantUsersView

app_name = 'users'
urlpatterns = [

    # ~ U S E R S

    path(
        'users/',
        TenantUsersView.as_view(),
        name='tenant-users',
    ),
    path(
        'users/<uuid:tenant_user_id>/',
        TenantUserView.as_view(),
        name='tenant-user',
    ),

    # ~ C U S T O M E R S
    path(
        'customers/',
        TenantCustomersView.as_view(),
        name='tenant-customers',
    ),
    path(
        'customers/<uuid:tenant_customer_id>/',
        TenantCustomerView.as_view(),
        name='tenant-customer',
    ),
    # ~ P R O F I L E S

    path(
        'customer/profile/',
        view=TenantCustomerProfileView.as_view(),
        name='tenant-customer-profile',
    ),
    path(
        'user/profile/',
        view=TenantUserProfileView.as_view(),
        name='tenant-user-profile',
    ),
    path(
        'user/password/',
        view=TenantUserPasswordView.as_view(),
        name='tenant-user-password',
    ),
]

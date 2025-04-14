from typing import Callable, Optional

import pytest
from pytest_django.lazy_django import skip_if_no_django
from rest_framework_simplejwt.tokens import RefreshToken, Token

from rest_framework.test import APIClient

from src.common.database.models import TenantCustomerORM, TenantORM, TenantUserORM


@pytest.fixture()
def api_client() -> APIClient:
    skip_if_no_django()
    return APIClient()


@pytest.fixture()
def api_client_factory(
    api_client: APIClient,
    tenant_orm: TenantORM,
    tenant_user_orm: TenantUserORM,
) -> Callable:
    def _api_client_factory(
        authenticated: bool = False,
        has_tenant: bool = False,
        is_owner: bool = False,
        extra_tenant: Optional[TenantORM] = None,
        extra_tenant_user: Optional[TenantUserORM] = None,
    ) -> APIClient:
        final_tenant_user_orm: TenantUserORM = extra_tenant_user or tenant_user_orm
        final_tenant_orm = extra_tenant or tenant_orm

        refresh_token: Token = RefreshToken.for_user(final_tenant_user_orm.user)
        access_token = 'Bearer {0}'.format(str(refresh_token.access_token))

        if authenticated:
            api_client.credentials(HTTP_AUTHORIZATION=access_token)

        if has_tenant:
            api_client.credentials(
                HTTP_AUTHORIZATION=access_token,
                HTTP_X_TENANT=final_tenant_orm.slug,
            )

        if is_owner:
            final_tenant_user_orm.tenant.owner = final_tenant_user_orm.user
            final_tenant_user_orm.tenant.save(update_fields=['owner'])

        return api_client

    return _api_client_factory


@pytest.fixture()
def auth_api_client(api_client_factory) -> APIClient:
    return api_client_factory(authenticated=True)


@pytest.fixture()
def tenant_api_client(api_client_factory) -> APIClient:
    return api_client_factory(
        authenticated=True,
        has_tenant=True,
    )


@pytest.fixture()
def owner_api_client(api_client_factory) -> APIClient:
    return api_client_factory(
        authenticated=True,
        has_tenant=True,
        is_owner=True,
    )


@pytest.fixture()
def unauthorized_api_client(
    api_client_factory: Callable,
    extra_tenant_orm: TenantORM,
    extra_tenant_customer_orm: TenantCustomerORM,
) -> APIClient:
    return api_client_factory(
        authenticated=True,
        has_tenant=True,
        extra_tenant_customer=extra_tenant_customer_orm,
    )


@pytest.fixture()
def external_api_client(
    api_client_factory: Callable,
    extra_tenant_orm: TenantORM,
    extra_tenant_customer_orm: TenantCustomerORM,
) -> APIClient:
    return api_client_factory(
        authenticated=True,
        has_tenant=True,
        extra_tenant=extra_tenant_orm,
        extra_tenant_customer=extra_tenant_customer_orm,
    )

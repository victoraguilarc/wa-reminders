from typing import Optional

from django.db.models import Q
from rest_framework.request import Request

from src.common.database.models import TenantCustomerORM, TenantORM, TenantUserORM, UserORM
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.entities.user import User
from src.common.infrastructure.builders.tenant import build_tenant
from src.common.infrastructure.builders.tenant_customer import build_tenant_customer
from src.common.infrastructure.builders.tenant_user import build_tenant_user
from src.common.infrastructure.builders.user import build_user
from src.common.presentation.api.exceptions.collection import (
    TENANT_CUSTOMER_NOT_FOUND,
    TENANT_NOT_FOUND,
    TENANT_USER_NOT_FOUND,
    USER_NOT_FOUND,
)
from src.common.presentation.constants import HTTP_TENANT_HEADER
from src.common.presentation.utils.strings import is_valid_uuid


def get_tenant_from_request(
    request: Request,
    tenant_required: bool = False,
) -> Optional[Tenant]:
    tenant_slug = request.META.get(HTTP_TENANT_HEADER, '')

    try:
        tenant_criteria = Q(slug=tenant_slug)
        if is_valid_uuid(tenant_slug):
            tenant_criteria = tenant_criteria | Q(uuid=tenant_slug)
        orm_instance = TenantORM.objects.select_related('owner').get(tenant_criteria)
        return build_tenant(orm_instance)
    except (TenantORM.DoesNotExist, AttributeError):
        if tenant_required:
            raise TENANT_NOT_FOUND
        return None


def get_tenant_user_from_request(
    request: Request,
    tenant: Tenant,
    raise_exception: bool = False,
) -> Optional[TenantUser]:
    if not request.user.is_authenticated:
        return None
    try:
        orm_instance = TenantUserORM.objects.select_related(
            'tenant', 'user', 'user__email_address', 'user__phone_number'
        ).get(tenant_id=tenant.id, user=request.user)
        return build_tenant_user(orm_instance)
    except TenantUserORM.DoesNotExist:
        if raise_exception:
            raise TENANT_USER_NOT_FOUND
        return None


def get_tenant_customer_from_request(
    request: Request,
    tenant: Tenant,
    raise_exception: bool = False,
) -> Optional[TenantCustomer]:
    if not request.user.is_authenticated:
        return None
    try:
        orm_instance = TenantCustomerORM.objects.select_related(
            'tenant', 'user', 'email_address', 'phone_number'
        ).get(tenant_id=tenant.id, user=request.user)
        return build_tenant_customer(orm_instance)
    except TenantCustomerORM.DoesNotExist:
        if raise_exception:
            raise TENANT_CUSTOMER_NOT_FOUND
        return None


def get_user_from_request(
    request: Request,
    raise_exception: bool = False,
) -> Optional[User]:
    if not request.user.is_authenticated:
        return None

    try:
        orm_instance = UserORM.objects.get(uuid=request.user.uuid)
        return build_user(orm_instance)
    except UserORM.DoesNotExist:
        if raise_exception:
            raise USER_NOT_FOUND
        return None

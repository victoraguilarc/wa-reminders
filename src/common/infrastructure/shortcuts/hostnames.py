from typing import Dict

from django.conf import settings

from src.common.application.shortcuts.customers_site import build_customers_site_url
from src.common.domain.enums.auth import PendingActionNamespace
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import TenantId
from src.pending_actions.domain.callback_builder import CallbackBuilder
from src.pending_actions.infrastructure.callback_builder import (
    DjangoCallbackBuilder,
    QueryParamsCallbackBuilder,
    PathCallbackBuilder,
)


def get_hostnames_map(
    query_bus: QueryBus,
    tenant_id: TenantId,
) -> Dict[PendingActionNamespace, CallbackBuilder]:
    return {
        PendingActionNamespace.TENANTS: DjangoCallbackBuilder(
            hostname=settings.API_HOSTNAME,
            view_name='auth:pending-action',
        ),
        PendingActionNamespace.TENANT_USERS: PathCallbackBuilder(
            hostname=settings.BACKOFFICE_HOSTNAME,
        ),
        PendingActionNamespace.TENANT_CUSTOMERS: QueryParamsCallbackBuilder(
            hostname=build_customers_site_url(
                query_bus=query_bus,
                tenant_id=tenant_id,
                fallback_url=settings.PAGES_ROOT_HOSTNAME,
            ),
        ),
    }

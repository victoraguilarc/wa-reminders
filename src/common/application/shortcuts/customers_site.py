from typing import Optional

from src.common.application.queries.tenants import (
    GetMembersSiteCallbackBuilderQuery,
)
from src.common.constants import DEFAULT_SESSION_REDEMPTION_SUB_PATH
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.value_objects import TenantId
from src.pending_actions.domain.callback_builder import CallbackBuilder


def get_members_callback_builder(
    query_bus: QueryBus,
    tenant_id: TenantId,
    sub_path: Optional[str] = None,
) -> Optional[CallbackBuilder]:
    return query_bus.ask(
        query=GetMembersSiteCallbackBuilderQuery(
            tenant_id=tenant_id,
            sub_path=sub_path,
        ),
    )

def get_members_session_callback_builder(
    query_bus: QueryBus,
    tenant_id: TenantId,
) -> Optional[CallbackBuilder]:
    return get_members_callback_builder(
        query_bus=query_bus,
        tenant_id=tenant_id,
        sub_path=DEFAULT_SESSION_REDEMPTION_SUB_PATH,
    )

from django.conf import settings

from src.common.application.commands.tenants import (
    DeactivateTenantCommand,
)
from src.common.application.queries.notifications import GetTenantWhatsappSessionNameQuery
from src.common.application.queries.tenants import (
    GetTenantByIdQuery,
    GetTenantContainerByIdQuery,
    GetMembersSiteCallbackBuilderQuery,
    GetUserTenantContainerQuery,
    GetUserTenantsQuery,
)
from src.common.infrastructure.context_builder import AppContextBuilder
from src.tenants.application.tenants.handlers.deactivate_tenant import DeactivateTenantCommandHandler
from src.tenants.application.tenants.handlers.get_callback_url import (
    GetMembersSiteCallbackBuilderHandler,
)
from src.tenants.application.tenants.handlers.get_tenant import (
    GetTenantByIdHandler,
    GetTenantContainerByIdHandler,
)
from src.tenants.application.tenants.handlers.get_user_tenant import (
    GetUserTenantContainerHandler,
    GetUserTenantsHandler,
)
from src.tenants.application.whatsapp_sessions.handlers.get_session_name import (
    GetTenantWhatsappSessionNameHandler,
)


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    # ~ C O M M A N D S

    bus.command_bus.subscribe(
        command=DeactivateTenantCommand,
        handler=DeactivateTenantCommandHandler(
            repository=domain_context.tenant_repository,
        ),
    )

    # ~ Q U E R I E S

    bus.query_bus.subscribe(
        query=GetTenantByIdQuery,
        handler=GetTenantByIdHandler(domain_context.tenant_repository),
    )
    bus.query_bus.subscribe(
        query=GetTenantContainerByIdQuery,
        handler=GetTenantContainerByIdHandler(domain_context.tenant_repository),
    )
    bus.query_bus.subscribe(
        query=GetUserTenantsQuery,
        handler=GetUserTenantsHandler(domain_context.tenant_repository),
    )
    bus.query_bus.subscribe(
        query=GetUserTenantContainerQuery,
        handler=GetUserTenantContainerHandler(domain_context.tenant_repository),
    )
    bus.query_bus.subscribe(
        query=GetMembersSiteCallbackBuilderQuery,
        handler=GetMembersSiteCallbackBuilderHandler(
            tenant_repository=domain_context.tenant_repository,
            fallback_hostname=settings.PAGES_ROOT_HOSTNAME,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantWhatsappSessionNameQuery,
        handler=GetTenantWhatsappSessionNameHandler(
            repository=domain_context.whatsapp_session_repository,
        ),
    )






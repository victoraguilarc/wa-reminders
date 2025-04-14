from uuid import UUID

from src.common.domain.context.locale import LocaleContext
from src.common.domain.data.countries import DEFAULT_COUNTRY_CONFIG
from src.common.domain.enums.locales import Language, TimeZone
from src.common.domain.value_objects import NotificationId, TenantId
from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.application.use_cases import NotificationPerformer

app_context = AppContextBuilder.from_env()
domain_context, bus_context = app_context.domain, app_context.bus

locale_context = LocaleContext(
    time_zone=TimeZone.UTC, language=Language.EN, country_config=DEFAULT_COUNTRY_CONFIG
)


def perform_notification(
    tenant_id: UUID,
    notification_id: UUID,
):
    app_service = NotificationPerformer(
        tenant_id=TenantId(tenant_id),
        notification_id=NotificationId(notification_id),
        notification_repository=domain_context.notification_repository,
        notification_recipient_repository=domain_context.notification_recipient_repository,
        command_bus=bus_context.command_bus,
    )

    response = app_service.execute()
    return response.render(locale_context)

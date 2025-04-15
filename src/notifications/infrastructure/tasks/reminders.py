from typing import Optional

import django_rq

from src.common.application.queries.notifications import GetTenantWhatsappSessionNameQuery
from src.common.domain.entities.reminder import Reminder
from src.common.infrastructure.context_builder import AppContextBuilder
from src.notifications.application.reminders.use_cases.performer import ReminderPerformer
from src.tenants.domain.exceptions import TenantWhatsappSessionNotFoundError


def perform_reminder(reminder: Reminder):
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    whatsapp_session: Optional[str] = bus.query_bus.ask(
        query=GetTenantWhatsappSessionNameQuery(
            tenant_id=reminder.tenant_id,
        ),
    )

    if not whatsapp_session:
        raise TenantWhatsappSessionNotFoundError

    ReminderPerformer(
        reminder_id=reminder.id,
        repository=domain_context.reminder_repository,
        whatsapp_sender=domain_context.whatsapp_sender,
        whatsapp_session=whatsapp_session,
    ).execute()


def create_reminder_job(reminder: Reminder) -> str:
    scheduler = django_rq.get_scheduler('default')
    scheduled_job = scheduler.enqueue_at(reminder.scheduled_time, perform_reminder, reminder.id)

    import ipdb;
    ipdb.set_trace()

    return "job_id_placeholder"


def update_reminder_job(reminder: Reminder) -> str:
    return "job_id_placeholder"


def cancel_reminder_job(reminder: Reminder) :
    return "job_id_placeholder"

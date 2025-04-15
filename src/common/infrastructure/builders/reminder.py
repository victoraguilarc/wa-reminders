from django.db.models import QuerySet

from src.common.database.models.reminder import ReminderORM, ReminderRecipientORM
from src.common.domain.entities.reminder import Reminder, ReminderRecipient
from src.common.domain.enums.reminders import ReminderStatus, ReminderRecipientStatus
from src.common.domain.value_objects import ReminderId, TenantId, ReminderRecipientId
from src.common.infrastructure.builders.phone_number import build_phone_number


def build_reminder(
    orm_instance: ReminderORM,
    orm_recipients: QuerySet[ReminderORM] | None = None,
) -> Reminder:
    orm_recipients = orm_recipients or []
    return Reminder(
        id=ReminderId(orm_instance.id),
        tenant_id=TenantId(orm_instance.tenant_id),
        job_id=orm_instance.job_id,
        content=orm_instance.content,
        scheduled_time=orm_instance.scheduled_time,
        status=ReminderStatus.from_value(orm_instance.status),
        recipients=[
            build_reminder_recipient(recipient)
            for recipient in orm_recipients
        ],
    )


def build_reminder_recipient(
    orm_instance: ReminderRecipientORM,
) -> ReminderRecipient:
    return ReminderRecipient(
        id=ReminderRecipientId(orm_instance.id),
        phone_number=build_phone_number(orm_instance.phone_number),
        status=ReminderRecipientStatus.from_value(orm_instance.status),
    )

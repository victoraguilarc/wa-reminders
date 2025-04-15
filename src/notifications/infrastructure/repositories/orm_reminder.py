

from typing import List, Optional

from src.common.database.models.reminder import ReminderORM, ReminderRecipientORM
from src.common.domain.entities.reminder import Reminder
from src.common.domain.value_objects import ReminderId, TenantId
from src.common.infrastructure.builders.reminder import build_reminder
from src.notifications.domain.repositories.reminder import ReminderRepository


class ORMReminderRepository(ReminderRepository):
    def find(self, instance_id: ReminderId) -> Optional[Reminder]:
        try:
            orm_instance = ReminderORM.objects.get(id=instance_id)
            orm_recipients = ReminderORM.objects.filter(reminder=orm_instance)
            return build_reminder(
                orm_instance=orm_instance,
                orm_recipients=orm_recipients,
            )
        except Exception as e:
            return None

    def persist(self, instance: Reminder) -> Reminder:
        orm_instance, created = ReminderORM.objects.update_or_create(
            id=instance.id,
            defaults={
                "tenant_id": instance.tenant_id,
                "content": instance.content,
                "scheduled_time": instance.scheduled_time,
                "status": str(instance.status),
            },
        )

        if instance.recipients:
            ReminderORM.objects.filter(reminder=orm_instance).delete()
            orm_recipients = [
                ReminderRecipientORM(
                    reminder=orm_instance,
                    phone_number_id=recipient.phone_number.id,
                    status=str(recipient.status),
                )
                for recipient in instance.recipients
            ]
            ReminderRecipientORM.objects.bulk_create(orm_recipients)

        orm_recipients = ReminderORM.objects.filter(reminder=orm_instance)
        return build_reminder(
            orm_instance=orm_instance,
            orm_recipients=orm_recipients,
        )

    def delete(self, instance_id: ReminderId):
        ReminderRecipientORM.objects.filter(reminder_id=instance_id).delete()
        ReminderORM.objects.filter(id=instance_id).delete()

    def filter(self, tenant_id: TenantId) -> List[Reminder]:
        orm_instances = ReminderORM.objects.filter(tenant_id=tenant_id)
        return [
            build_reminder(orm_instance=orm_instance)
            for orm_instance in orm_instances
        ]



from typing import List, Optional

from src.common.database.models.reminder import ReminderORM, ReminderRecipientORM
from src.common.domain.entities.reminder import Reminder, ReminderRecipient
from src.common.domain.value_objects import ReminderId, TenantId
from src.common.infrastructure.builders.reminder import build_reminder, build_reminder_recipient
from src.notifications.domain.repositories.reminder import ReminderRepository


class ORMReminderRepository(ReminderRepository):
    def find(self, instance_id: ReminderId) -> Optional[Reminder]:
        try:
            orm_instance = ReminderORM.objects.get(uuid=instance_id)
            orm_recipients = ReminderRecipientORM.objects.filter(reminder=orm_instance)

            return build_reminder(
                orm_instance=orm_instance,
                orm_recipients=orm_recipients,
            )
        except Exception as e:
            return None

    def persist(
        self,
        instance: Reminder,
        persist_recipients: bool = True,
    ) -> Reminder:
        persist_dict = {
            "tenant_id": instance.tenant_id,
            "content": instance.content,
            "scheduled_time": instance.scheduled_time,
            "scheduled_job_id": instance.scheduled_job_id,
        }
        if instance.status:
            persist_dict["status"] = str(instance.status)

        orm_instance, created = ReminderORM.objects.update_or_create(
            uuid=instance.id,
            defaults=persist_dict,
        )

        if persist_recipients and instance.recipients:
            ReminderRecipientORM.objects.filter(reminder=orm_instance).delete()
            orm_recipients = [
                ReminderRecipientORM(
                    reminder=orm_instance,
                    phone_number_id=recipient.phone_number.id,
                )
                for recipient in instance.recipients
            ]
            ReminderRecipientORM.objects.bulk_create(orm_recipients)

        orm_recipients = ReminderRecipientORM.objects.filter(reminder=orm_instance)
        return build_reminder(
            orm_instance=orm_instance,
            orm_recipients=orm_recipients,
        )

    def persist_recipient(
        self,
        instance: ReminderRecipient,
    ) -> ReminderRecipient:
        orm_instance, created = ReminderRecipientORM.objects.update_or_create(
            uuid=instance.id,
            defaults={
                "phone_number_id": instance.phone_number.id,
                "status": str(instance.status),
            },
        )
        return build_reminder_recipient(orm_instance=orm_instance)

    def delete(self, instance_id: ReminderId):
        ReminderRecipientORM.objects.filter(reminder_id=instance_id).delete()
        ReminderORM.objects.filter(uuid=instance_id).delete()

    def filter(self, tenant_id: TenantId) -> List[Reminder]:
        orm_instances = ReminderORM.objects.filter(tenant_id=tenant_id)
        return [
            build_reminder(orm_instance=orm_instance)
            for orm_instance in orm_instances
        ]

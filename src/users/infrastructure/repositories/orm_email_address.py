# -*- coding: utf-8 -*-

from typing import Optional

from src.common.database.models import EmailAddressORM
from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.value_objects import EmailAddressId
from src.common.infrastructure.builders.email_address import build_email_address
from src.users.domain.repositories.email_address import EmailAddressRepository


class ORMEmailAddressRepository(EmailAddressRepository):
    def find(
        self,
        email: str,
    ) -> Optional[EmailAddress]:
        try:
            orm_instance = EmailAddressORM.objects.get(email=email)
            return build_email_address(orm_instance)
        except EmailAddressORM.DoesNotExist:
            return None

    def get_or_create(
        self,
        email: str,
    ) -> EmailAddress:
        orm_instance, _ = EmailAddressORM.objects.get_or_create(
            email=email,
        )
        return build_email_address(orm_instance)

    def persist(
        self,
        instance: EmailAddress,
    ) -> EmailAddress:
        orm_instance, _ = EmailAddressORM.objects.update_or_create(
            email=instance.email,
            defaults=instance.to_persist_dict,
        )
        return build_email_address(orm_instance)

    def delete(
        self,
        instance_id: EmailAddressId,
    ):
        EmailAddressORM.objects.filter(id=instance_id).delete()

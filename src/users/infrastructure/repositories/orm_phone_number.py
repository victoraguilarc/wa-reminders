# -*- coding: utf-8 -*-

from typing import Optional

from src.common.database.models import PhoneNumberORM
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.value_objects import PhoneNumberId, RawPhoneNumber
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.users.domain.repositories.phone_number import PhoneNumberRepository


class ORMPhoneNumberRepository(PhoneNumberRepository):
    def find(
        self,
        dial_code: int,
        phone_number: str,
    ) -> Optional[PhoneNumber]:
        try:
            orm_instance = PhoneNumberORM.objects.get(
                dial_code=dial_code,
                phone_number=phone_number,
            )
            return build_phone_number(orm_instance)
        except PhoneNumberORM.DoesNotExist:
            return None


    def get_or_create(
        self,
        raw_phone_number: RawPhoneNumber,
    ) -> PhoneNumber:
        orm_instance, _ = PhoneNumberORM.objects.get_or_create(
            dial_code=raw_phone_number.dial_code,
            phone_number=raw_phone_number.phone_number,
            defaults=raw_phone_number.to_persist_dict,
        )
        return build_phone_number(orm_instance)

    def persist(
        self,
        instance: PhoneNumber,
    ) -> PhoneNumber:
        orm_instance, _ = PhoneNumberORM.objects.update_or_create(
            dial_code=instance.dial_code,
            phone_number=instance.phone_number,
            defaults=instance.to_persist_dict,
        )
        return build_phone_number(orm_instance)

    def delete(
        self,
        instance_id: PhoneNumberId,
    ):
        PhoneNumberORM.objects.filter(id=instance_id).delete()

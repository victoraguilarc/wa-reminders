# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.value_objects import PhoneNumberId, RawPhoneNumber


class PhoneNumberRepository(ABC):
    @abstractmethod
    def find(
        self,
        dial_code: int,
        phone_number: str,
    ) -> Optional[PhoneNumber]:
        raise NotImplementedError

    @abstractmethod
    def get_or_create(
        self,
        raw_phone_number: RawPhoneNumber,
    ) -> PhoneNumber:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        instance: PhoneNumber,
    ) -> PhoneNumber:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        instance_id: PhoneNumberId,
    ):
        raise NotImplementedError

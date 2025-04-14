# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

from src.common.domain.models.email_address import EmailAddress
from src.common.domain.value_objects import EmailAddressId


class EmailAddressRepository(ABC):
    @abstractmethod
    def find(
        self,
        email: str,
    ) -> Optional[EmailAddress]:
        raise NotImplementedError

    @abstractmethod
    def get_or_create(
        self,
        email: str,
    ) -> EmailAddress:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        instance: EmailAddress,
    ) -> EmailAddress:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        instance_id: EmailAddressId,
    ):
        raise NotImplementedError

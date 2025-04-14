from abc import ABC, abstractmethod
from typing import Optional

from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.user import User
from src.common.domain.value_objects import RawPhoneNumber, UserId


class UserRepository(ABC):
    @abstractmethod
    def find(
        self,
        user_id: UserId,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_phone_number(
        self,
        phone_number: RawPhoneNumber,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def persist_phone_number(
        self,
        phone_number: PhoneNumber,
    ) -> Optional[PhoneNumber]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        instance: User,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def set_password(
        self,
        user_id: UserId,
        new_password: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        instance: User,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_user_context(
        self,
        user_id: UserId,
    ) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        user_id: UserId,
    ):
        raise NotImplementedError

from typing import Optional

from src.common.database.models import PhoneNumberORM, TenantCustomerORM, UserORM
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.value_objects import RawPhoneNumber, UserId
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.common.infrastructure.builders.user import build_user
from src.users.domain.repositories.user import UserRepository


class ORMUserRepository(UserRepository):
    def find(self, user_id: UserId) -> Optional[User]:
        try:
            orm_instance = (
                UserORM.objects
                .select_related(*self._get_select_related())
                .get(uuid=str(user_id))
            )
            return build_user(orm_instance)
        except UserORM.DoesNotExist:
            return None

    def find_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        try:
            orm_instance = (
                UserORM.objects
                .select_related(*self._get_select_related())
                .get(email_address__email=email)
            )
            return build_user(orm_instance)
        except UserORM.DoesNotExist:
            return None

    def find_by_phone_number(
        self,
        phone_number: RawPhoneNumber,
    ) -> Optional[User]:
        try:
            orm_instance = UserORM.objects.get(
                phone_number__phone_number=phone_number.phone_number,
                phone_number__dial_code=phone_number.dial_code,
            )
            return build_user(orm_instance)
        except UserORM.DoesNotExist:
            return None

    def persist_phone_number(
        self,
        phone_number: PhoneNumber,
    ) -> Optional[PhoneNumber]:
        try:
            orm_instance, _ = PhoneNumberORM.objects.get_or_create(
                dial_code=phone_number.dial_code,
                phone_number=phone_number.phone_number,
                defaults=phone_number.to_persist_dict,
            )
            return build_phone_number(orm_instance)
        except PhoneNumberORM.DoesNotExist:
            return None

    def register(self, instance: User) -> User:
        orm_instance, _ = UserORM.objects.get_or_create(
            email=instance.email,
            defaults=instance.to_persist_dict,
        )
        return build_user(orm_instance)

    def set_password(
        self,
        user_id: UserId,
        new_password: str,
    ) -> bool:
        try:
            orm_instance = UserORM.objects.get(uuid=str(user_id))
            orm_instance.set_password(new_password)
            orm_instance.save()
            return True
        except UserORM.DoesNotExist:
            return False

    def persist(self, instance: User) -> User:
        orm_instance, _ = UserORM.objects.update_or_create(
            uuid=instance.id,
            defaults=instance.to_persist_dict,
        )
        return build_user(orm_instance)

    def find_user_context(
        self,
        user_id: UserId,
    ) -> Optional[UserContext]:
        try:
            orm_instance = UserORM.objects.get(uuid=user_id)
            user = build_user(orm_instance)
            return UserContext(user=user, profile=user.profile)
        except TenantCustomerORM.DoesNotExist:
            return None

    def delete(self, user_id: UserId):
        try:
            orm_instance = UserORM.objects.get(uuid=user_id)
            orm_instance.delete()
        except UserORM.DoesNotExist:
            return None

    @classmethod
    def _get_select_related(cls):
        return (
            'email_address',
            'phone_number',
        )

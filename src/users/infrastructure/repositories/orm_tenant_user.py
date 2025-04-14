# -*- coding: utf-8 -*-

from typing import List, Optional

from django.db.models import Q, QuerySet, Value
from django.db.models.functions import Concat

from src.common.database.models import EmailAddressORM, PhoneNumberORM, TenantUserORM, UserORM
from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.pagination import Page
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.value_objects import RawPhoneNumber, TenantId, TenantUserId, UserId
from src.common.infrastructure.builders.email_address import build_email_address
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.common.infrastructure.builders.tenant_user import build_tenant_user
from src.common.infrastructure.builders.user import build_user
from src.common.infrastructure.mixins.pagination import ORMPaginationMixin
from src.users.domain.filters.tenant_users import TenantUsersFilters
from src.users.domain.repositories.tenant_user import TenantUserRepository


class ORMTenantUserRepository(ORMPaginationMixin, TenantUserRepository):
    def find(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
    ) -> Optional[TenantUser]:
        tenant_user_orm = self._get_tenant_user_orm(tenant_id, tenant_user_id)
        if not tenant_user_orm:
            return None
        return build_tenant_user(tenant_user_orm)

    def find_user_context(
        self,
        tenant_id: TenantId,
        user_id: UserId,
    ) -> Optional[UserContext]:
        try:
            orm_instance = TenantUserORM.objects.get(
                user_id=user_id,
                tenant_id=tenant_id,
            )
            tenant_user = build_tenant_user(orm_instance)
            return UserContext(user=tenant_user.user, profile=tenant_user.profile)
        except TenantUserORM.DoesNotExist:
            return None

    def is_phone_number_available(
        self,
        tenant_id: TenantId,
        dial_code: int,
        phone_number: str,
        excluded_ids: List[TenantUserId] = None,
    ) -> bool:
        excluded_ids = excluded_ids or []
        return not (
            TenantUserORM.objects.exclude(uuid__in=excluded_ids)
            .filter(
                tenant_id=tenant_id,
                user__phone_number__dial_code=dial_code,
                user__phone_number__phone_number=phone_number,
            )
            .exists()
        )

    def is_email_available(
        self,
        tenant_id: TenantId,
        email: str, excluded_ids: List[TenantUserId] = None,
    ) -> bool:
        excluded_ids = excluded_ids or []
        return not (
            TenantUserORM.objects.exclude(uuid__in=excluded_ids)
            .filter(
                tenant_id=tenant_id,
                user__email_address__email=email,
            )
            .exists()
        )

    def find_by_email(
        self,
        email: str,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[TenantUser]:
        try:
            orm_instance = TenantUserORM.objects.select_related(*self._get_select_related()).get(
                user__email_address__email=email,
                tenant_id=tenant_id,
            )
            return build_tenant_user(orm_instance)
        except TenantUserORM.DoesNotExist:
            return None

    def find_by_phone_number(
        self,
        tenant_id: TenantId,
        phone_number: RawPhoneNumber,
    ) -> Optional[TenantUser]:
        try:
            orm_instance = TenantUserORM.objects.select_related(*self._get_select_related()).get(
                tenant_id=tenant_id,
                user__phone_number__phone_number=phone_number.phone_number,
                user__phone_number__dial_code=phone_number.dial_code,
            )
            return build_tenant_user(orm_instance)
        except TenantUserORM.DoesNotExist:
            return None

    def filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantUsersFilters,
    ) -> List[TenantUser]:
        orm_instances = self._filter(tenant_id, list_filters)
        return [build_tenant_user(orm_instance) for orm_instance in orm_instances]

    def filter_paginated(
        self,
        tenant_id: TenantId,
        list_filters: TenantUsersFilters,
    ) -> Page:
        orm_instances = self._filter(tenant_id, list_filters)
        return self._get_pagination_page(
            query_set=orm_instances,
            page_params=list_filters.page_params,
            domain_builder=build_tenant_user,
        )

    def filter_by_ids(
        self,
        tenant_id: TenantId,
        tenant_user_ids: List[TenantUserId],
    ) -> List[TenantUser]:
        orm_instances = TenantUserORM.objects.select_related(*self._get_select_related()).filter(
            tenant__uuid=tenant_id,
            uuid__in=tenant_user_ids,
        )
        return [build_tenant_user(orm_instance) for orm_instance in orm_instances]

    def filter_by_tenant(
        self,
        tenant_id: TenantId,
    ) -> List[TenantUser]:
        orm_instances = TenantUserORM.objects.select_related(*self._get_select_related()).filter(
            tenant_id=tenant_id
        )
        return [build_tenant_user(orm_instance) for orm_instance in orm_instances]

    def persist(self, instance: TenantUser) -> TenantUser:
        instance.user = self._persist_user(instance.user)
        persisted_instance, _ = TenantUserORM.objects.update_or_create(
            uuid=instance.id,
            tenant_id=instance.tenant_id,
            defaults=instance.to_persist_dict,
        )
        return build_tenant_user(persisted_instance)

    def check_password(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
        current_password: str,
    ) -> bool:
        tenant_user_orm = self._get_tenant_user_orm(tenant_id, tenant_user_id)
        return tenant_user_orm.user.check_password(current_password)

    def update_password(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
        new_password: str,
    ):
        tenant_user_orm = self._get_tenant_user_orm(tenant_id, tenant_user_id)
        tenant_user_orm.user.set_password(new_password)
        tenant_user_orm.user.save()

    def create_from_user(
        self,
        tenant_id: TenantId,
        user_id: UserId,
        status: TenantUserStatus,
        is_owner: bool,
    ) -> TenantUser:
        persisted_instance, _ = TenantUserORM.objects.get_or_create(
            tenant_id=tenant_id,
            user_id=user_id,
            defaults={
                'status': status.value,
                'is_owner': is_owner,
            },
        )
        return build_tenant_user(persisted_instance)

    def delete(
        self,
        tenant_id: TenantId,
        tenant_user_id: TenantUserId,
    ):
        tenant_user_orm = self._get_tenant_user_orm(tenant_id, tenant_user_id)
        if not tenant_user_orm:
            return
        if tenant_user_orm and tenant_user_orm.photo:
            tenant_user_orm.photo.delete()
        tenant_user_orm.delete()

    def _filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantUsersFilters,
    ) -> QuerySet[TenantUserORM]:
        filter_criteria = Q(tenant_id=tenant_id)
        filter_annotations = dict(
            complete_name=Concat(
                'first_name',
                Value(' '),
                'paternal_surname',
                Value(' '),
                'maternal_surname',
            ),
        )
        if list_filters.statuses:
            filter_criteria &= Q(status__in=[status.value for status in list_filters.statuses])
        if list_filters.search_term:
            filter_criteria &= (
                Q(complete_name__unaccent__icontains=list_filters.search_term)
                | Q(user__phone_number__phone_number__icontains=list_filters.search_term)
                | Q(user__email_address__email__icontains=list_filters.search_term)
            )

        return (
            TenantUserORM.objects
            .select_related(*self._get_select_related())
            .annotate(**filter_annotations)
            .filter(filter_criteria)
            .order_by('-created_at')
        )

    @classmethod
    def _persist_user(cls, user: User) -> User:
        email_address = cls._persist_email_address(user)
        phone_number = cls._persist_phone_number(user)

        user_orm, _ = UserORM.objects.get_or_create(uuid=user.id)

        if (
            email_address
            and email_address.id != user_orm.email_address_id
            and cls._is_email_available(email_address)
        ):
            user_orm.email_address_id = email_address.id

        if (
            phone_number
            and phone_number.id != user_orm.phone_number_id
            and cls._is_phone_available(phone_number)
        ):
            user_orm.phone_number_id = phone_number.id

        user_orm.save()
        return build_user(user_orm)

    @classmethod
    def _is_email_available(cls, email_address: EmailAddress) -> bool:
        return not UserORM.objects.filter(email_address__email=email_address.email).exists()

    @classmethod
    def _is_phone_available(cls, phone_number: PhoneNumber) -> bool:
        return not UserORM.objects.filter(
            phone_number__dial_code=phone_number.dial_code,
            phone_number__phone_number=phone_number.phone_number,
        ).exists()

    @classmethod
    def _get_user_from_same(
        cls,
        email_address: Optional[EmailAddress] = None,
        phone_number: Optional[PhoneNumber] = None,
    ):
        if not email_address and not phone_number:
            return None
        try:
            user_orm = UserORM.objects.get(
                email_address__email=email_address.email,
                phone_number__dial_code=phone_number.dial_code,
                phone_number__phone_number=phone_number.phone_number,
            )
            return build_user(user_orm)
        except UserORM.DoesNotExist:
            return None

    @classmethod
    def _get_user_from_many(
        cls,
        email_address: Optional[EmailAddress] = None,
        phone_number: Optional[PhoneNumber] = None,
    ):
        if not email_address and not phone_number:
            return None
        email_user_orm, _ = UserORM.objects.get_or_create(
            email_address_id=email_address.id,
            defaults={},
        )
        phone_user_orm, _ = UserORM.objects.get_or_create(
            phone_number_id=phone_number.id,
            defaults={},
        )

    @classmethod
    def _persist_phone_number(
        cls,
        user: User,
    ) -> Optional[PhoneNumber]:
        if not user.phone_number:
            return None
        phone_number, _ = PhoneNumberORM.objects.update_or_create(
            phone_number=user.phone_number.phone_number,
            dial_code=user.phone_number.dial_code,
            defaults=user.phone_number.to_raw_persist_dict,
        )
        return build_phone_number(phone_number)

    @classmethod
    def _persist_email_address(
        cls,
        user: User,
    ) -> Optional[EmailAddress]:
        if not user.email_address:
            return None
        email_address, _ = EmailAddressORM.objects.get_or_create(
            email=user.email_address.email,
        )
        return build_email_address(email_address)

    @classmethod
    def _get_select_related(cls):
        return (
            'tenant',
            'role',
            'user',
            'user__email_address',
            'user__phone_number',
        )

    @classmethod
    def _get_tenant_user_orm(
        cls,
        tenant_id: TenantId,
        instance_id: TenantUserId,
    ) -> Optional[TenantUserORM]:
        try:
            return TenantUserORM.objects.get(
                tenant_id=tenant_id,
                uuid=instance_id,
            )
        except TenantUserORM.DoesNotExist:
            return None

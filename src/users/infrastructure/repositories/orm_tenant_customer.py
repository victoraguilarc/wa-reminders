# -*- coding: utf-8 -*-

from typing import List, Optional
from uuid import uuid4

from django.db.models import Q, QuerySet, Value
from django.db.models.functions import Concat

from src.common.database.models import (
    EmailAddressORM,
    PhoneNumberORM,
    TenantCustomerORM,
    UserORM,
)
from src.common.domain.enums.users import TenantCustomerStatus, TenantCustomerCreationSource
from src.common.domain.entities.email_address import EmailAddress
from src.common.domain.entities.list_filters import ListFilters
from src.common.domain.entities.pagination import Page
from src.common.domain.entities.phone_number import PhoneNumber
from src.common.domain.entities.simple_person import SimplePerson
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.user import User
from src.common.domain.entities.user_context import UserContext
from src.common.domain.value_objects import (
    RawPhoneNumber,
    TenantCustomerId,
    TenantId,
    UserId,
)
from src.common.infrastructure.builders.email_address import build_email_address
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.common.infrastructure.builders.tenant_customer import build_tenant_customer
from src.common.infrastructure.builders.user import build_user
from src.common.infrastructure.mixins.pagination import ORMPaginationMixin
from src.users.domain.filters.tenant_customers import TenantCustomersFilters
from src.users.domain.repositories.tenant_customer import TenantCustomerRepository


class ORMTenantCustomerRepository(ORMPaginationMixin, TenantCustomerRepository):
    def delete(
        self,
        tenant_id: TenantId,
        tenant_customer_id: TenantCustomerId,
    ):
        TenantCustomerORM.objects.filter(
            uuid=tenant_customer_id,
            tenant_id=tenant_id,
        ).delete()

    def find(
        self,
        tenant_id: TenantId,
        tenant_customer_id: Optional[TenantCustomerId],
    ) -> Optional[TenantCustomer]:
        if not tenant_customer_id:
            return None
        try:
            orm_instance = TenantCustomerORM.objects.get(
                uuid=tenant_customer_id,
                tenant_id=tenant_id,
            )
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def find_by_params(
        self,
        tenant_id: TenantId,
        tenant_customer_id: Optional[TenantCustomerId] = None,
        email: Optional[str] = None,
        phone_number: Optional[RawPhoneNumber] = None,
    ) -> Optional[TenantCustomer]:
        return (
            self.find(tenant_id=tenant_id, tenant_customer_id=tenant_customer_id)
            or self.find_by_phone_number(tenant_id=tenant_id, phone_number=phone_number)
            or self.find_by_email(tenant_id=tenant_id, email=email)
        )

    def find_for_session(
        self,
        tenant_id: TenantId,
        email: Optional[str] = None,
        raw_phone_number: Optional[RawPhoneNumber] = None,
    ) -> Optional[TenantCustomer]:
        if not email and not raw_phone_number:
            return None

        filter_criteria = Q(tenant_id=tenant_id)
        if email:
            filter_criteria &= Q(email_address__email=email)
        if raw_phone_number:
            filter_criteria &= Q(
                phone_number__phone_number=raw_phone_number.phone_number,
                phone_number__dial_code=raw_phone_number.dial_code,
            )
        try:
            orm_instance = (
                TenantCustomerORM.objects
                .select_related(*self._get_select_related())
                .get(filter_criteria)
            )
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None


    def find_by_access_code(
        self,
        tenant_id: TenantId,
        access_code: str,
    ) -> Optional[TenantCustomer]:
        try:
            orm_instance = (
                TenantCustomerORM.objects
                .select_related(*self._get_select_related())
                .get(
                    tenant_id=tenant_id,
                    access_code__code=access_code,
                )
            )
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def find_user_context(self, user_id: UserId, tenant_id: TenantId) -> Optional[UserContext]:
        try:
            orm_instance = TenantCustomerORM.objects.get(
                user_id=user_id,
                tenant_id=tenant_id,
            )
            tenant_customer = build_tenant_customer(orm_instance)
            return UserContext(user=tenant_customer.user, profile=tenant_customer.profile)
        except TenantCustomerORM.DoesNotExist:
            return None

    def is_phone_number_available(
        self,
        tenant_id: TenantId,
        dial_code: int,
        phone_number: str,
        excluded_ids: List[TenantCustomerId] = None,
    ) -> bool:
        excluded_ids = excluded_ids or []
        return not (
            TenantCustomerORM.objects.exclude(uuid__in=excluded_ids)
            .filter(
                tenant_id=tenant_id,
                phone_number__dial_code=dial_code,
                phone_number__phone_number=phone_number,
            )
            .exists()
        )

    def is_email_available(
        self, tenant_id: TenantId, email: str, excluded_ids: List[TenantCustomerId] = None
    ) -> bool:
        excluded_ids = excluded_ids or []
        return not (
            TenantCustomerORM.objects.exclude(uuid__in=excluded_ids)
            .filter(
                tenant_id=tenant_id,
                email_address__email=email,
            )
            .exists()
        )

    def find_by_email(
        self,
        email: Optional[str],
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[TenantCustomer]:
        if not email:
            return None
        try:
            orm_instance = TenantCustomerORM.objects.select_related(
                *self._get_select_related()
            ).get(
                email_address__email=email,
                tenant_id=tenant_id,
            )
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def find_by_phone_number(
        self,
        tenant_id: TenantId,
        phone_number: Optional[RawPhoneNumber],
    ) -> Optional[TenantCustomer]:
        if not phone_number:
            return None
        try:
            orm_instance = TenantCustomerORM.objects.select_related(
                *self._get_select_related()
            ).get(
                tenant_id=tenant_id,
                phone_number__phone_number=phone_number.phone_number,
                phone_number__dial_code=phone_number.dial_code,
            )
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def find_by_alias(
        self,
        tenant_id: TenantId,
        alias: str,
    ) -> Optional[TenantCustomer]:
        filter_criteria = Q(tenant_id=tenant_id, alias=alias)
        try:
            orm_instance = TenantCustomerORM.objects.select_related('user').get(filter_criteria)
            return build_tenant_customer(orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomersFilters,
    ) -> List[TenantCustomer]:
        orm_instances = self._filter(tenant_id, list_filters)
        return [build_tenant_customer(orm_instance) for orm_instance in orm_instances]

    def filter_paginated(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomersFilters,
    ) -> Page:
        orm_instances = self._filter(tenant_id, list_filters)
        return self._get_pagination_page(
            query_set=orm_instances,
            page_params=list_filters.page_params,
            domain_builder=build_tenant_customer,
        )

    def filter_by_ids(
        self,
        tenant_id: TenantId,
        tenant_customer_ids: List[TenantCustomerId],
    ) -> List[TenantCustomer]:
        orm_instances = TenantCustomerORM.objects.select_related(
            *self._get_select_related()
        ).filter(
            tenant__uuid=tenant_id,
            uuid__in=tenant_customer_ids,
        )
        return [build_tenant_customer(orm_instance) for orm_instance in orm_instances]

    def filter_by_tenant(
        self,
        tenant_id: TenantId,
    ) -> List[TenantCustomer]:
        orm_instances = TenantCustomerORM.objects.select_related(
            *self._get_select_related()
        ).filter(tenant_id=tenant_id)
        return [build_tenant_customer(orm_instance) for orm_instance in orm_instances]

    def persist(self, instance: TenantCustomer) -> TenantCustomer:
        instance.user = self._persist_user(instance.user)
        instance.email_address = self._persist_email_address(instance)
        instance.phone_number = self._persist_phone_number(instance)

        persisted_instance, _ = TenantCustomerORM.objects.update_or_create(
            uuid=instance.id,
            tenant_id=instance.tenant_id,
            defaults=instance.to_persist_dict,
        )
        return build_tenant_customer(persisted_instance)

    def get_or_create_from_person(
        self,
        tenant_id: TenantId,
        person: SimplePerson,
        tenant_customer_id: Optional[TenantCustomerId] = None,
        status: Optional[TenantCustomerStatus] = None,
        creation_source: Optional[TenantCustomerCreationSource] = None,
    ) -> TenantCustomer:
        defaults = dict(
            first_name=person.first_name,
            paternal_surname=person.paternal_surname,
            maternal_surname=person.maternal_surname,
        )

        tenant_customer_orm = self._find_by_email_or_phone_number(
            tenant_id=tenant_id,
            email=person.email,
            phone_number=person.phone_number,
        )

        # TODO: Update this section to verify active memberships as needed
        if tenant_customer_orm:
            return build_tenant_customer(orm_instance=tenant_customer_orm)

        defaults['status'] = str(status) if status else str(TenantCustomerStatus.ACTIVE)
        defaults['uuid'] = tenant_customer_id or uuid4()

        if creation_source:
            defaults['creation_source'] = str(creation_source)

        if person.email:
            email_address = self._get_or_create_email_address(person.email)
            defaults['email_address_id'] = email_address.id

        if person.phone_number:
            phone_number = self._get_or_create_phone_number(person.phone_number)
            defaults['phone_number_id'] = phone_number.id

        user_instance = UserORM.objects.create(is_active=True)
        new_tenant_customer_orm = TenantCustomerORM.objects.create(
            tenant_id=tenant_id,
            user_id=user_instance.uuid,
            **defaults,
        )

        return build_tenant_customer(orm_instance=new_tenant_customer_orm)


    def create_from_user(
        self,
        tenant_id: TenantId,
        user_id: UserId,
        status: TenantCustomerStatus,
    ) -> TenantCustomer:
        persisted_instance, _ = TenantCustomerORM.objects.get_or_create(
            tenant_id=tenant_id,
            user_id=user_id,
            defaults={
                'status': status.value,
            },
        )
        return build_tenant_customer(persisted_instance)

    def _filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomersFilters,
    ) -> QuerySet[TenantCustomerORM] | None:
        filter_criteria = Q(tenant_id=tenant_id)
        filter_annotations = dict(
            complete_name=Concat(
                'first_name',
                Value(' '),
                'paternal_surname',
                Value(' '),
                'maternal_surname',
            )
        )

        if list_filters.search_term:
            filter_criteria &= (
                Q(complete_name__unaccent__icontains=list_filters.search_term)
                | Q(phone_number__phone_number__icontains=list_filters.search_term)
                | Q(email_address__email__icontains=list_filters.search_term)
            )

        if list_filters.statuses:
            filter_criteria &= Q(status__in=[str(status) for status in list_filters.statuses])

        return (
            TenantCustomerORM.objects
            .select_related(*self._get_select_related())
            .annotate(**filter_annotations)
            .filter(filter_criteria)
            .order_by('-created_at')
        )

    @classmethod
    def _find_by_email_or_phone_number(
        cls,
        tenant_id: TenantId,
        email: Optional[str] = None,
        phone_number: Optional[RawPhoneNumber] = None,
    ) -> Optional[TenantCustomerORM]:
        filter_criteria = Q(tenant_id=tenant_id)
        email_criteria = Q(email_address__email=email) if email else Q()
        phone_number_criteria = (
            (
                Q(
                    phone_number__phone_number=phone_number.phone_number,
                    phone_number__dial_code=phone_number.dial_code,
                )
            )
            if phone_number
            else Q()
        )
        return TenantCustomerORM.objects.filter(
            filter_criteria & (email_criteria | phone_number_criteria)
        ).first()

    @classmethod
    def _persist_user(cls, user: User) -> User:
        user_orm, _ = UserORM.objects.update_or_create(
            uuid=user.id,
            defaults=user.to_persist_dict,
        )
        return build_user(user_orm)

    @classmethod
    def _get_or_create_phone_number(
        cls,
        raw_phone_number: RawPhoneNumber,
    ) -> PhoneNumber:
        phone_number, _ = PhoneNumberORM.objects.get_or_create(
            phone_number=raw_phone_number.phone_number,
            dial_code=raw_phone_number.dial_code,
            defaults=raw_phone_number.to_persist_dict,
        )
        return build_phone_number(phone_number)

    @classmethod
    def _persist_phone_number(
        cls,
        tenant_customer: TenantCustomer,
    ) -> Optional[PhoneNumber]:
        if not tenant_customer.phone_number:
            return None
        phone_number, _ = PhoneNumberORM.objects.update_or_create(
            phone_number=tenant_customer.phone_number.phone_number,
            dial_code=tenant_customer.phone_number.dial_code,
            defaults=tenant_customer.phone_number.to_raw_persist_dict,
        )
        return build_phone_number(phone_number)

    @classmethod
    def _get_or_create_email_address(cls, email: str) -> EmailAddress:
        email_address, _ = EmailAddressORM.objects.get_or_create(email=email)
        return build_email_address(email_address)

    @classmethod
    def _persist_email_address(
        cls,
        tenant_customer: TenantCustomer,
    ) -> Optional[EmailAddress]:
        if not tenant_customer.email_address:
            return None
        email_address, _ = EmailAddressORM.objects.get_or_create(
            email=tenant_customer.email_address.email,
        )
        return build_email_address(email_address)

    @classmethod
    def _clean_photo(cls, tenant_customer: TenantCustomer):
        if tenant_customer.created_at is None:
            return
        orm_instance = TenantCustomerORM.objects.get(uuid=tenant_customer.id)
        orm_instance.photo.delete()

    @classmethod
    def _get_select_related(cls):
        return 'user', 'tenant', 'email_address', 'phone_number', 'access_code'

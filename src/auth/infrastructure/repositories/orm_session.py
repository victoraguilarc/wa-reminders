# -*- coding: utf-8 -*-

from typing import List, Optional

from django.db.models import Q

from src.auth.domain.repositories.session import SessionRepository
from src.common.database.models import (
    EmailAddressORM,
    PhoneNumberORM,
    TenantCustomerORM,
    TenantORM,
    TenantUserORM,
    UserORM,
)
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.models.user import User
from src.common.domain.models.user_context import UserContext
from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.value_objects import EmailAddressId, PhoneNumberId, TenantId, UserId
from src.common.infrastructure.builders.email_address import build_email_address
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.common.infrastructure.builders.tenant import build_tenant
from src.common.infrastructure.builders.tenant_customer import build_tenant_customer
from src.common.infrastructure.builders.tenant_user import build_tenant_user
from src.common.infrastructure.builders.user import build_user


class ORMSessionRepository(SessionRepository):
    def estimate_current_tenant(self, user: User) -> Optional[Tenant]:
        user_orm = self._find(user.id)
        if not user_orm.current_tenant:
            last_owned_tenant = (
                TenantORM.objects.filter(owner_id=user.id).order_by('created_at').first()
            )
            last_tenant_customer = (
                TenantCustomerORM.objects.filter(user_id=user.id).order_by('-created_at').first()
            )
            tenant_customer_tenant = last_tenant_customer.tenant if last_tenant_customer else None
            user_orm.current_tenant = last_owned_tenant or tenant_customer_tenant
            user_orm.save(update_fields=['current_tenant'])

        return build_tenant(user_orm.current_tenant) if user_orm.current_tenant else None

    def get_session_tenants(
        self,
        user: User,
    ) -> List[Tenant]:
        orm_instances = TenantORM.objects.filter(owner_id=user.uuid)
        return [build_tenant(orm_instance) for orm_instance in orm_instances]

    def find_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        user_orm = self._find_by_email(email)
        if not user_orm:
            return None
        return build_user(user_orm)

    def find_tenant_user(
        self,
        user_id: UserId,
        tenant_id: TenantId,
    ) -> Optional[TenantUser]:
        try:
            orm_instance = TenantUserORM.objects.select_related(
                'user',
                'user__phone_number',
                'user__email_address',
            ).get(
                tenant_id=tenant_id,
                user_id=user_id,
                status=str(TenantUserStatus.ACTIVE),
            )
            return build_tenant_user(orm_instance=orm_instance)
        except TenantUserORM.DoesNotExist:
            return None

    def find_tenant_customer(
        self,
        user_id: UserId,
        tenant_id: TenantId,
    ) -> Optional[TenantCustomer]:
        try:
            orm_instance = TenantCustomerORM.objects.select_related(
                'user', 'phone_number', 'email_address'
            ).get(
                tenant_id=tenant_id,
                user_id=user_id,
            )
            return build_tenant_customer(orm_instance=orm_instance)
        except TenantCustomerORM.DoesNotExist:
            return None

    def find_context_by_email(
        self,
        email: str,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[UserContext]:
        user = self.find_by_email(email)
        if not user:
            return None
        tenant_user = self.find_tenant_user(user.id, tenant_id)
        return UserContext(
            user=user,
            profile=tenant_user.profile if tenant_user else user.profile,
        )

    def find(
        self,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[User]:
        if tenant_id:
            return self._get_from_tenant_customer_by_id(user_id, tenant_id)
        return self._get_from_user_by_id(user_id)

    def find_context(
        self,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[UserContext]:
        if tenant_id:
            return self._get_context_from_tenant_customer_by_id(user_id, tenant_id)
        return self._get_context_from_user_by_id(user_id)

    def find_email_address(
        self,
        email_address_id: EmailAddressId,
    ) -> Optional[EmailAddress]:
        try:
            orm_instance = EmailAddressORM.objects.get(uuid=email_address_id)
            return build_email_address(orm_instance=orm_instance)
        except EmailAddressORM.DoesNotExist:
            return None

    def find_phone_number(
        self,
        phone_number_id: PhoneNumberId,
    ) -> Optional[PhoneNumber]:
        try:
            orm_instance = PhoneNumberORM.objects.get(uuid=phone_number_id)
            return build_phone_number(orm_instance=orm_instance)
        except PhoneNumberORM.DoesNotExist:
            return None

    def has_valid_password(
        self,
        user: User,
        password: str,
    ) -> bool:
        user_orm = self._find(user.id)
        return user_orm.check_password(password)

    @classmethod
    def _find(cls, user_id: UserId) -> Optional[UserORM]:
        try:
            return UserORM.objects.select_related('phone_number').get(uuid=user_id)
        except UserORM.DoesNotExist:
            return None

    @classmethod
    def _find_by_email(cls, email: str) -> Optional[UserORM]:
        try:
            return UserORM.objects.select_related('phone_number', 'email_address').get(
                email_address__email=email
            )
        except UserORM.DoesNotExist:
            return None

    @classmethod
    def _get_from_user_by_email(cls, email: str) -> Optional[User]:
        user_orm = UserORM.objects.select_related('phone_number').filter(email=email).first()
        if not user_orm:
            return None
        return build_user(user_orm)

    @classmethod
    def _get_from_tenant_customer_by_email(cls, email: str) -> Optional[User]:
        tenant_customer_orm = TenantCustomerORM.objects.filter(user__email=email).first()
        if not tenant_customer_orm:
            return None
        return build_tenant_customer(orm_instance=tenant_customer_orm).user

    @classmethod
    def _get_from_user_by_id(cls, user_id: UserId) -> Optional[User]:
        user_orm = UserORM.objects.select_related('phone_number').filter(uuid=user_id).first()
        if not user_orm:
            return None
        return build_user(orm_instance=user_orm)

    @classmethod
    def _get_from_tenant_customer_by_id(
        cls,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[User]:
        filter_criteria = Q(user_id=user_id)
        if tenant_id:
            filter_criteria &= Q(tenant_id=tenant_id)

        tenant_customer_orm = TenantCustomerORM.objects.filter(filter_criteria).first()
        if not tenant_customer_orm:
            return None

        tenant_customer = build_tenant_customer(orm_instance=tenant_customer_orm)
        return tenant_customer.user

    @classmethod
    def _get_context_from_user_by_id(
        cls,
        user_id: UserId,
    ) -> Optional[UserContext]:
        user_orm = UserORM.objects.select_related('phone_number').filter(uuid=user_id).first()
        if not user_orm:
            return None

        user = build_user(orm_instance=user_orm)
        return UserContext(
            user=user,
            profile=user.profile,
        )

    @classmethod
    def _get_context_from_tenant_customer_by_id(
        cls,
        user_id: UserId,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[UserContext]:
        filter_criteria = Q(user_id=user_id)
        if tenant_id:
            filter_criteria &= Q(tenant_id=tenant_id)

        tenant_customer_orm = TenantCustomerORM.objects.filter(filter_criteria).first()
        if not tenant_customer_orm:
            return None

        tenant_customer = build_tenant_customer(orm_instance=tenant_customer_orm)
        return UserContext(
            user=tenant_customer.user,
            profile=tenant_customer.profile,
        )

# -*- coding: utf-8 -*-

from typing import List, Optional, Union

from django.db.models import QuerySet

from src.common.database.models import (
    TenantORM,
    TenantUserORM,
    UserORM, TenantWhatsappSessionORM,
)
from src.common.domain.entities.list_filters import ListFilters
from src.common.domain.entities.pagination import Page
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_wa_session import TenantWhatsappSession
from src.common.domain.enums.tenants import TenantStatus
from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.value_objects import TenantId, TenantSlug, UserId
from src.common.infrastructure.builders.tenant import build_tenant
from src.common.infrastructure.builders.tenant_wa_session import build_tenant_whatsapp_session
from src.common.infrastructure.mixins.pagination import ORMPaginationMixin
from src.tenants.domain.repositories.tenant import TenantRepository


class ORMTenantRepository(ORMPaginationMixin, TenantRepository):
    def find(self, tenant_id: TenantId) -> Optional[Tenant]:
        tenant = self._find(tenant_id)
        if not tenant:
            return None
        return build_tenant(tenant)

    def find_by_slug(self, slug: TenantSlug) -> Optional[Tenant]:
        try:
            orm_instance = self._get_tenant_objects().get(slug=slug)
            return build_tenant(orm_instance)
        except TenantORM.DoesNotExist:
            return None

    def find_by_wa_session(
        self,
        session_name: str,
    ) -> Optional[TenantWhatsappSession]:
        try:
            orm_instance = (
                TenantWhatsappSessionORM.objects
                .select_related('tenant')
                .get(session_name=session_name)
            )
            return build_tenant_whatsapp_session(orm_instance)
        except TenantWhatsappSessionORM.DoesNotExist:
            return None

    def get_tenants_counter(self, user_id: UserId) -> int:
        return TenantORM.objects.filter(owner_id=user_id).count()


    def get_active_tenants(self) -> List[Tenant]:
        orm_instances = self._get_tenant_objects().filter(
            status__in=[TenantStatus.ACTIVE],
        )
        return [build_tenant(orm_instance) for orm_instance in orm_instances]

    def find_by_id(self, tenant_id: TenantId) -> Optional[Tenant]:
        try:
            orm_instance = self._get_tenant_objects().get(uuid=tenant_id)
            return build_tenant(orm_instance)
        except TenantORM.DoesNotExist:
            return None

    def persist(self, tenant: Tenant) -> Tenant:
        return build_tenant(self._persist(tenant))

    def get_user_tenants(self, user_id: UserId) -> List[Tenant]:
        orm_instances = self._get_user_tenants(user_id)
        return [build_tenant(orm_instance) for orm_instance in orm_instances]

    def get_user_tenants_paginated(
        self,
        user_id: UserId,
        list_filters: ListFilters,
    ) -> Page:
        orm_instances = self._get_user_tenants(user_id)
        return self._get_pagination_page(
            query_set=orm_instances,
            page_params=list_filters.page_params,
            domain_builder=build_tenant,
        )

    def switch_tenant(self, user_id: UserId, tenant_id: TenantId):
        UserORM.objects.filter(uuid=user_id).update(current_tenant_id=tenant_id)


    def get_owners_count(self, tenant_id: TenantId) -> int:
        return TenantUserORM.objects.filter(
            tenant_id=tenant_id,
            status=str(TenantUserStatus.ACTIVE),
            is_owner=True,
        ).count()

    @classmethod
    def _get_tenant_objects(cls) -> QuerySet:
        return TenantORM.objects.select_related('tenant_tier')

    def _get_user_tenants(self, user_id: UserId) -> Union[QuerySet, List[Tenant]]:
        tenant_uuids = (
            TenantUserORM.objects.select_related('tenant')
            .filter(
                user_id=user_id,
                status=str(TenantUserStatus.ACTIVE),
            )
            .values_list('tenant', flat=True)
            .order_by('-created_at')
        )
        return self._get_tenant_objects().filter(uuid__in=tenant_uuids)

    @classmethod
    def _find(cls, tenant_id: TenantId) -> Optional[TenantORM]:
        try:
            return cls._get_tenant_objects().get(uuid=tenant_id)
        except TenantORM.DoesNotExist:
            return None

    @classmethod
    def _find_user(cls, user_id: UserId) -> Optional[UserORM]:
        try:
            return UserORM.objects.select_related('phone_number').get(uuid=user_id)
        except UserORM.DoesNotExist:
            return None

    @classmethod
    def _persist(cls, tenant: Tenant) -> TenantORM:
        if tenant.is_new:
            slug_count = TenantORM.objects.filter(slug__startswith=tenant.slug).count()
            tenant_slug = f'{tenant.slug}-{slug_count}' if slug_count > 0 else tenant.slug
            orm_instance = TenantORM.objects.create(
                name=tenant.name,
                slug=tenant_slug,
                owner_id=tenant.owner_id,
                status=str(tenant.status),
                lang=str(tenant.lang),
                country_iso_code=str(tenant.country_iso_code),
                currency_code=str(tenant.currency_code),
                timezone=str(tenant.timezone),
                logo=tenant.logo,
            )
            UserORM.objects.filter(uuid=tenant.owner_id).update(
                current_tenant_id=orm_instance.uuid,
            )
        else:
            orm_instance, _ = TenantORM.objects.update_or_create(
                uuid=tenant.id,
                defaults=tenant.to_persist_dict,
            )
        return orm_instance

# -*- coding: utf-8 -*-

from typing import List, Optional

from django.db.models import Q

from src.common.database.models import TenantCustomerLeadORM, MembershipTenantCustomerORM
from src.common.domain.enums.growth import TenantLeadStage
from src.common.domain.models.pagination import Page
from src.common.domain.models.tenant_customer_lead import TenantCustomerLead
from src.common.domain.value_objects import TenantCustomerId, TenantId, TenantCustomerLeadId
from src.common.infrastructure.builders.tenant_customer_lead import build_tenant_customer_lead
from src.common.infrastructure.mixins.pagination import ORMPaginationMixin
from src.users.domain.filters.tenant_customer_leads import TenantCustomerLeadsFilters
from src.users.domain.repositories.tenant_customer_lead import TenantCustomerLeadRepository


class ORMTenantCustomerLeadRepository(
    ORMPaginationMixin,
    TenantCustomerLeadRepository,
):
    def filter(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomerLeadsFilters,
    ) -> List[TenantCustomerLead]:
        orm_instances = self._get_filter_queryset(tenant_id, list_filters)
        return [build_tenant_customer_lead(orm_instance) for orm_instance in orm_instances]

    def filter_page(
        self,
        tenant_id: TenantId,
        list_filters: TenantCustomerLeadsFilters,
    ) -> Page:
        return self._get_pagination_page(
            page_params=list_filters.page_params,
            query_set=self._get_filter_queryset(tenant_id, list_filters), # noqa
            domain_builder=build_tenant_customer_lead,
            lookup_field='-created_at',
        )

    def find(
        self,
        tenant_id: TenantId,
        instance_id: TenantCustomerId,
    ) -> Optional[TenantCustomerLead]:
        try:
            orm_instance = (
                TenantCustomerLeadORM.objects
                .select_related(*self._get_select_related())
                .get(
                    uuid=instance_id,
                    tenant_id=tenant_id,
                )
            )
            return build_tenant_customer_lead(orm_instance)
        except TenantCustomerLeadORM.DoesNotExist:
            return None

    def find_by_email(
        self,
        email: str,
        tenant_id: Optional[TenantId] = None,
    ) -> Optional[TenantCustomerLead]:
        try:
            orm_instance = (
                TenantCustomerLeadORM.objects
                .select_related(*self._get_select_related())
                .get(
                    email=email,
                    tenant_id=tenant_id,
                )
            )
            return build_tenant_customer_lead(orm_instance)
        except TenantCustomerLeadORM.DoesNotExist:
            return None

    def find_by_tenant_customer(
        self,
        tenant_id: TenantId,
        tenant_customer_id: TenantCustomerId,
    ) -> Optional[TenantCustomerLead]:
        try:
            orm_instance = (
                TenantCustomerLeadORM.objects
                .select_related(*self._get_select_related())
                .get(
                    tenant_customer_id=tenant_customer_id,
                    tenant_id=tenant_id,
                )
            )
            return build_tenant_customer_lead(orm_instance)
        except TenantCustomerLeadORM.DoesNotExist:
            return None

    def persist(
        self,
        tenant_id: TenantId,
        instance: TenantCustomerLead,
    ) -> TenantCustomerLead:
        persisted_instance, _ = TenantCustomerLeadORM.objects.update_or_create(
            uuid=instance.id,
            tenant_id=tenant_id,
            defaults=instance.to_persist_dict,
        )
        return build_tenant_customer_lead(persisted_instance)

    def persist_by_customer(
        self,
        tenant_id: TenantId,
        instance: TenantCustomerLead,
    ) -> TenantCustomerLead:
        persisted_instance, _ = TenantCustomerLeadORM.objects.update_or_create(
            tenant_customer_id=instance.tenant_customer.id,
            tenant_id=tenant_id,
            defaults={
                'channel': str(instance.channel) if instance.channel else None,
                'stage': str(instance.stage) if instance.stage else str(TenantLeadStage.CREATED),
            },
        )
        return build_tenant_customer_lead(
            orm_instance=persisted_instance,
            customer_has_memberships=self._get_has_memberships(persisted_instance.tenant_customer_id),
        )

    # TODO: Delete it after removing usage
    # def create_from_simple_person(
    #     self,
    #     tenant_id: TenantId,
    #     person: SimplePerson,
    #     channel: Optional[TenantLeadChannel] = None,
    #     status: Optional[TenantLeadStage] = None,
    # ) -> TenantCustomerLead:
    #     persisted_instance, _ = TenantCustomerLeadORM.objects.get_or_create(
    #         tenant_id=tenant_id,
    #         email=person.email,
    #         defaults={
    #             'first_name': person.first_name,
    #             'paternal_surname': person.paternal_surname,
    #             'maternal_surname': person.maternal_surname,
    #             'channel': str(channel) if channel else None,
    #             'status': str(status) if status else str(TenantLeadStage.CREATED),
    #         },
    #     )
    #     return build_tenant_customer_lead(persisted_instance)

    def delete(
        self,
        tenant_id: TenantId,
        instance_id: TenantCustomerLeadId,
    ):
        TenantCustomerLeadORM.objects.filter(
            uuid=instance_id,
            tenant_id=tenant_id,
        ).delete()

    @classmethod
    def _get_filter_queryset(
        cls,
        tenant_id: TenantId,
        list_filters: TenantCustomerLeadsFilters,
    ):
        filter_criteria = Q(tenant_id=tenant_id)

        if list_filters.search_term:
            filter_criteria &= (
                Q(first_name__icontains=list_filters.search_term)
                | Q(paternal_surname__icontains=list_filters.search_term)
                | Q(maternal_surname__icontains=list_filters.search_term)
            )

        if list_filters.channels:
            filter_criteria &= Q(channel__in=[str(channel) for channel in list_filters.channels])

        if list_filters.statuses:
            filter_criteria &= Q(status__in=[str(status) for status in list_filters.statuses])

        return (
            TenantCustomerLeadORM.objects
            .select_related(*cls._get_select_related())
            .filter(filter_criteria)
        )

    @classmethod
    def _get_select_related(cls):
        return (
            'tenant',
            'tenant_customer',
            'tenant_customer__phone_number',
            'tenant_customer__email_address',
        )


    @classmethod
    def _get_has_memberships(cls, tenant_customer_id: TenantCustomerId) -> bool:
        return MembershipTenantCustomerORM.objects.filter(
            tenant_customer_id=tenant_customer_id,
        ).exists()

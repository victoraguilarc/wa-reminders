# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Dict, List

from src.common.application.queries.memberships import GetMembershipsPendingPaymentsQuery
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.interfaces.services import ApiService
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.list_filters import ListFilters
from src.common.domain.models.meta_membership import MetaMembership
from src.common.domain.models.pagination import Page
from src.common.domain.models.payment_request import PaymentRequest
from src.common.domain.value_objects import TenantCustomerId, TenantId, MembershipId
from src.users.domain.repositories import TenantCustomerRepository


@dataclass
class TenantCustomerMembershipsLister(ApiService):
    tenant_id: TenantId
    tenant_customer_id: TenantCustomerId
    list_filters: ListFilters
    repository: TenantCustomerRepository
    currency_code: CurrencyCode
    query_bus: QueryBus
    include_pending_payments: bool = False

    def execute(self, *args, **kwargs) -> Page:
        current_page = self.repository.get_memberhips_paginated(
            tenant_id=self.tenant_id,
            tenant_customer_id=self.tenant_customer_id,
            list_filters=self.list_filters,
        )
        if self.include_pending_payments:
            return self._enrich_page(current_page)
        return current_page

    def _enrich_page(self, current_page: Page):
        membership_ids = [membership.id for membership in current_page.items]
        pending_payments_map: Optional[Dict[MembershipId, List[PaymentRequest]]] = self.query_bus.ask(
            query=GetMembershipsPendingPaymentsQuery(
                tenant_id=self.tenant_id,
                currency_code=self.currency_code,
                membership_ids=membership_ids,
            )
        )
        current_page.items = [
            MetaMembership(
                membership=membership,
                pending_payments=pending_payments_map.get(membership.id, []),
            )
            for membership in current_page.items
        ]
        return current_page

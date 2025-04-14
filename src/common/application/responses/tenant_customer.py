# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from src.common.application.presenters.tenant_customer import (
    TenantCustomerPresenter,
)
from src.common.constants import INSTANCE_DELETED_RESPONSE
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.models.tenant_customer import TenantCustomer


@dataclass
class TenantCustomerResponse(ApiResponse):
    instance: Optional[TenantCustomer] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:
        if not self.instance:
            return INSTANCE_DELETED_RESPONSE
        return TenantCustomerPresenter(self.instance, locale_context).to_dict


@dataclass
class TenantCustomersResponse(ApiResponse):
    instances: List[TenantCustomer]

    def render(self, locale_context: LocaleContext) -> Union[Dict, List]:
        return [
            TenantCustomerPresenter(instance, locale_context).to_dict for instance in self.instances
        ]

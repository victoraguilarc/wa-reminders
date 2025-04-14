# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from src.common.application.presenters.tenant import TenantPresenter
from src.common.constants import INSTANCE_DELETED_RESPONSE
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.models.tenant import Tenant


@dataclass
class TenantResponse(ApiResponse):
    instance: Optional[Tenant] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:
        if not self.instance:
            return INSTANCE_DELETED_RESPONSE
        return TenantPresenter(self.instance, locale_context).to_dict



@dataclass
class TenantsResponse(ApiResponse):
    instances: List[Tenant]

    def render(self, locale_context: LocaleContext) -> list:
        return [TenantPresenter(instance, locale_context).to_dict for instance in self.instances]

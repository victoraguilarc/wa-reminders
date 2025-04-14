# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from src.common.application.presenters.tenant_user import TenantUserPresenter
from src.common.constants import INSTANCE_DELETED_RESPONSE
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.models.tenant_user import TenantUser


@dataclass
class TenantUserResponse(ApiResponse):
    instance: Optional[TenantUser] = None

    def render(self, locale_context: LocaleContext) -> Union[Dict, str]:
        if not self.instance:
            return INSTANCE_DELETED_RESPONSE
        return TenantUserPresenter(
            instance=self.instance,
            locale_context=locale_context,
        ).to_dict


@dataclass
class TenantUsersResponse(ApiResponse):
    instances: List[TenantUser]

    def render(self, locale_context: LocaleContext) -> Union[dict, list]:
        return [
            TenantUserPresenter(
                instance=instance,
                locale_context=locale_context,
            ).to_dict
            for instance in self.instances
        ]

# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.presenters.profile import UserProfilePresenter
from src.common.application.presenters.tenant import TenantPresenter
from src.common.application.presenters.tenant_container import UserTenantContainerPresenter
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.entities.user_profile_container import UserProfileContainer


@dataclass
class UserProfileContainerResponse(ApiResponse):
    instance: UserProfileContainer

    def render(self, locale_context: LocaleContext) -> dict:
        return {
            'profile': UserProfilePresenter(self.instance.user_profile).to_dict,
            'tenant': (
                UserTenantContainerPresenter(
                    instance=self.instance.current_tenant,
                    locale_context=locale_context,
                ).to_dict
                if self.instance.current_tenant
                else None
            ),
            'tenants': [
                TenantPresenter(tenant, locale_context).to_dict for tenant in self.instance.tenants
            ],
        }

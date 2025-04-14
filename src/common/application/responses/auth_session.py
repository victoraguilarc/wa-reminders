# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.presenters.profile import UserProfilePresenter
from src.common.application.presenters.tenant_customer import TenantCustomerPresenter
from src.common.application.presenters.tenant_user import TenantUserPresenter
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.models.user_profile import UserProfile
from src.common.domain.models.user_session import TenantCustomerSession, TenantUserSession


@dataclass
class TenantUserSessionResponse(ApiResponse):
    instance: TenantUserSession

    def render(self, locale_context: LocaleContext) -> dict:
        data = {
            'profile': TenantUserPresenter(self.instance.profile, locale_context).to_dict,
            # 'tenant': (
            #     UserTenantContainerPresenter(
            #         instance=self.instance.current_tenant,
            #         locale_context=locale_context,
            #     ).to_dict
            #     if self.instance.current_tenant
            #     else None
            # ),
        }
        if self.instance.token:
            data['session'] = self.instance.token
        return data


@dataclass
class TenantCustomerSessionResponse(ApiResponse):
    instance: TenantCustomerSession

    def render(self, locale_context: LocaleContext) -> dict:
        return {
            'session': self.instance.token,
            'profile': TenantCustomerPresenter(self.instance.profile, locale_context).to_dict,
            # 'tenant': (
            #     UserTenantContainerPresenter(
            #         instance=self.instance.current_tenant,
            #         locale_context=locale_context,
            #     ).to_dict
            #     if self.instance.current_tenant
            #     else None
            # ),
        }


@dataclass
class UserProfileResponse(ApiResponse):
    instance: UserProfile

    def render(self, locale_context: LocaleContext) -> dict:
        return UserProfilePresenter(self.instance).to_dict

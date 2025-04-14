# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.entities.tenant_user import TenantUser
from src.common.helpers.time import TimeUtils


@dataclass
class TenantUserPresenterMixin(object):
    instance: TenantUser
    locale_context: LocaleContext

    def _build_data(self) -> dict:
        return {
            'id': str(self.instance.id),
            'user_id': str(self.instance.user.id),
            'status': str(self.instance.status),
            'email_address': (
                self.instance.email_address.to_minimal_dict if self.instance.email_address else None
            ),
            'phone_number': (
                self.instance.phone_number.to_minimal_dict if self.instance.phone_number else None
            ),
            'first_name': self.instance.first_name,
            'paternal_surname': self.instance.paternal_surname,
            'maternal_surname': self.instance.maternal_surname,
            'photo_url': self.instance.photo_url,

            'is_owner': self.instance.is_owner,
            'created_at': (
                TimeUtils.localize_isoformat(
                    date_time=self.instance.created_at,
                    time_zone=str(self.locale_context.time_zone),
                )
                if self.instance.created_at
                else None
            ),
        }


@dataclass
class TenantUserPresenter(TenantUserPresenterMixin):
    @property
    def to_dict(self) -> dict:
        data = self._build_data()
        return data



@dataclass
class TenantUserSessionConfigPresenter(TenantUserPresenterMixin):
    @property
    def to_dict(self) -> dict:
        return self._build_data()



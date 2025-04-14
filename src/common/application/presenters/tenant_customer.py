from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.helpers.time import TimeUtils


@dataclass
class TenantCustomerPresenter(object):
    instance: TenantCustomer
    locale_context: LocaleContext

    @property
    def to_dict(self) -> dict:
        return {
            'id': str(self.instance.id),
            'user_id': str(self.instance.user.id),
            'status': (
                str(self.instance.status)
                if self.instance.status else None
            ),
            'email_address': (
                self.instance.email_address.to_minimal_dict if self.instance.email_address else None
            ),
            'phone_number': (
                self.instance.phone_number.to_minimal_dict if self.instance.phone_number else None
            ),
            'first_name': self.instance.first_name,
            'paternal_surname': self.instance.paternal_surname,
            'maternal_surname': self.instance.maternal_surname,
            'birth_date': (
                TimeUtils.format_simple_date(self.instance.birth_date)
                if self.instance.birth_date
                else None
            ),
            'photo_url': self.instance.photo_url,
            'gender': (str(self.instance.gender) if self.instance.gender else None),
            'created_at': (
                TimeUtils.localize_isoformat(
                    date_time=self.instance.created_at,
                    time_zone=str(self.locale_context.time_zone),
                )
                if self.instance.created_at
                else None
            ),
            'display_name': self.instance.display_name,
            'display_email': self.instance.display_email,
            'display_phone': self.instance.display_phone,
        }

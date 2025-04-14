from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.models.tenant import Tenant
from src.common.domain.enums.currencies import CurrencyCode


@dataclass
class TenantPresenter(object):
    instance: Tenant
    locale_context: LocaleContext

    @property
    def to_dict(self) -> dict:
        return {
            'id': str(self.instance.id),
            'name': self.instance.name,
            'slug': self.instance.slug,
            'logo_url': self.instance.logo_url,
            'timezone': str(self.instance.timezone),
            'country_iso_code': str(self.instance.country_iso_code),
            'currency_code': str(self.instance.currency_code),
            'currency_symbol': CurrencyCode.get_symbol(self.instance.currency_code),
            'address': (
                self.instance.address.to_simple_dict
                if self.instance.address else None
            ),
        }

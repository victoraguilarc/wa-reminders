from dataclasses import dataclass
from typing import Optional

from src.common.constants import DEFAULT_LANGUAGE
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone, Language


@dataclass
class CountryConfig(object):
    name: str
    iso_code: CountryIsoCode
    currency_code: CurrencyCode
    dial_code: int
    time_zone: TimeZone
    emoji: str
    lang: Language = DEFAULT_LANGUAGE
    dial_prefix: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'CountryConfig':
        return cls(
            name=data.get('name'),
            iso_code=CountryIsoCode.from_value(data.get('iso_code')),
            currency_code=CurrencyCode.from_value(data.get('currency_code')),
            time_zone=TimeZone(data.get('time_zone')),
            dial_code=data.get('dial_code'),
            emoji=data.get('emoji'),
            dial_prefix=data.get('dial_prefix'),
        )

from src.common.constants import PHONE_NUMBER_PREFIXES_MAP
from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.value_objects import RawPhoneNumber


class RawPhoneNumberBuilder(object):
    @classmethod
    def build(
        cls,
        dial_code: int,
        phone_number: str,
    ) -> RawPhoneNumber:
        country_config = CountryConfigBuilder.from_dial_code(dial_code)
        prefixed_countries = PHONE_NUMBER_PREFIXES_MAP.keys()
        phone_number = RawPhoneNumber(
            dial_code=dial_code,
            phone_number=phone_number,
            iso_code=country_config.iso_code,
            prefix=None,
        )
        if country_config.iso_code in prefixed_countries:
            phone_number.prefix = PHONE_NUMBER_PREFIXES_MAP[country_config.iso_code]
        return phone_number

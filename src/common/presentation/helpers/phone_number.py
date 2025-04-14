from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.value_objects import RawPhoneNumber


def get_raw_phone_number(
    phone_number_data: dict,
) -> RawPhoneNumber:
    dial_code = phone_number_data.get('dial_code')
    country_config = CountryConfigBuilder.from_dial_code(dial_code)
    return RawPhoneNumber(
        dial_code=country_config.dial_code,
        phone_number=phone_number_data.get('phone_number'),
        iso_code=country_config.iso_code,
        prefix=country_config.dial_prefix,
    )

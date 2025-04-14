# -*- coding: utf-8 -*-
from src.common.application.helpers.time import utc_now
from src.common.domain.models.picture import Picture
from src.common.domain.models.tenant import Tenant
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone
from src.common.domain.value_objects import PictureId
from src.common.helpers.dicts import validate_mandatory


class TenantBuilder(object):
    @classmethod
    def load_props_from_payload(cls, tenant: Tenant, verified_data: dict) -> Tenant:
        tenant.name = (
            verified_data.get('name') if validate_mandatory(verified_data, 'name') else None
        )
        tenant.slug = (
            verified_data.get('slug') if validate_mandatory(verified_data, 'slug') else None
        )
        tenant.logo = (
            Picture(
                id=PictureId(verified_data.get('logo')),
                image_url='',
                created_at=utc_now(),
            )
            if validate_mandatory(verified_data, 'logo')
            else None
        )
        tenant.timezone = (
            TimeZone.from_value(verified_data.get('timezone'))
            if validate_mandatory(verified_data, 'timezone')
            else None
        )
        tenant.country_iso_code = (
            CountryIsoCode.from_value(verified_data.get('country_iso_code'))
            if validate_mandatory(verified_data, 'country_iso_code')
            else None
        )
        if validate_mandatory(verified_data, 'currency_code'):
            tenant.currency_code = CurrencyCode.from_value(verified_data.get('currency_code'))
            tenant.currency_symbol = CurrencyCode.get_symbol(tenant.currency_code)
        return tenant

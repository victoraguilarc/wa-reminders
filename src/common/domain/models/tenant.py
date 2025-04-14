# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass
from datetime import datetime
from io import FileIO
from typing import List, Optional

from slugify import slugify

from src.common.constants import (
    DEFAULT_COUNTRY_ISO_CODE,
    DEFAULT_MAX_FREE_TRIALS,
    DEFAULT_NUM_WHAPSAPP_SESSIONS, DEFAULT_CHECKIN_FROM_SESSIONS_IN_HOURS,
)
from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone, Language
from src.common.domain.enums.tenants import TenantStatus
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.models.country_config import CountryConfig
from src.common.domain.value_objects import TenantId, TenantSlug, TenantTierId, UserId
from src.common.helpers.dicts import validate_mandatory


@dataclass
class Tenant(AggregateRoot):
    id: TenantId
    name: str
    slug: TenantSlug
    status: TenantStatus
    timezone: TimeZone
    lang: Language
    currency_code: CurrencyCode
    country_iso_code: CountryIsoCode
    owner_id: Optional[UserId] = None
    currency_symbol: Optional[str] = None
    grace_period: Optional[int] = None
    reference: Optional[str] = None
    logo: Optional[FileIO] = None
    logo_url: Optional[str] = None
    tier_id: Optional[TenantTierId] = None
    created_at: Optional[datetime] = None
    refresh_expiration_on_passes: bool = False
    membership_changes_with_remaining: bool = False
    checkin_from_in_hours: int = DEFAULT_CHECKIN_FROM_SESSIONS_IN_HOURS
    checkin_until_in_hours: int = DEFAULT_CHECKIN_FROM_SESSIONS_IN_HOURS
    max_free_trials: int = DEFAULT_MAX_FREE_TRIALS
    num_whatsapp_sessions: int = DEFAULT_NUM_WHAPSAPP_SESSIONS

    @property
    def is_new(self) -> bool:
        return self.created_at is None

    @property
    def is_active(self) -> bool:
        return self.status == TenantStatus.ACTIVE

    @property
    def to_persist_dict(self) -> dict:
        return {
            'name': self.name,
            'slug': self.slug,
            'owner_id': self.owner_id,
            'status': str(self.status),
            'timezone': str(self.timezone),
            'lang': str(self.lang),
            'currency_code': str(self.currency_code),
            'country_iso_code': str(self.country_iso_code),
            'currency_symbol': self.currency_symbol,
            'grace_period': self.grace_period,
            'checkin_from_in_hours': self.checkin_from_in_hours,
            'checkin_until_in_hours': self.checkin_until_in_hours,
            'reference': self.reference,
            'tier_id': self.tier_id,
        }

    @classmethod
    def build_from_payload(cls, verified_data: dict) -> 'Tenant':
        name = verified_data.get('name', uuid.uuid4().hex)
        country_iso_code = CountryIsoCode.from_value(
            verified_data.get('country_iso_code', str(DEFAULT_COUNTRY_ISO_CODE))
        )
        country_config: CountryConfig = CountryConfigBuilder.from_iso_code(country_iso_code)
        return Tenant(
            id=TenantId(verified_data.get('id', uuid.uuid4())),
            name=name,
            owner_id=None,
            slug=TenantSlug(slugify(name)),
            timezone=country_config.time_zone,
            lang=country_config.lang,
            currency_code=country_config.currency_code,
            country_iso_code=country_iso_code,
            status=TenantStatus.ACTIVE,
            logo=(verified_data.get('logo') if validate_mandatory(verified_data, 'logo') else None),
        )

    def check_ownership(self, user_id: UserId) -> bool:
        return self.owner_id == user_id

    def overload(
        self,
        new_instance: 'Tenant',
        properties: List[str] = None,
    ):
        instance_properties = properties or [
            'name',
            'slug',
            'owner_id',
            'status',
            'timezone',
            'lang',
            'currency_code',
            'country_iso_code',
            'currency_symbol',
            'grace_period',
            'checkin_from_in_hours',
            'checkin_until_in_hours',
            'reference',
            'tier_id',
        ]
        for _property in instance_properties:
            property_value = getattr(new_instance, _property)
            if not property_value:
                continue
            setattr(self, _property, property_value)
        return self

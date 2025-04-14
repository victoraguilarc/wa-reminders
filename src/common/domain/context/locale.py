# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

from src.common.domain.context.client import ConsumerClient
from src.common.domain.entities.country_config import CountryConfig
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.enums.locales import Language, TimeZone
from src.common.domain.interfaces.locales import LocaleService


@dataclass
class LocaleContext(object):
    time_zone: TimeZone
    language: Language
    country_config: CountryConfig
    locale_service: Optional[LocaleService] = None
    client: Optional[ConsumerClient] = None


@dataclass
class TenantContext(object):
    tenant: Optional[Tenant] = None
    tenant_user: Optional[TenantUser] = None
    tenant_customer: Optional[TenantCustomer] = None

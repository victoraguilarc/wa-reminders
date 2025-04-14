# -*- coding: utf-8 -*-

from dataclasses import dataclass
from decimal import Decimal

from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.payments import TimePeriod
from src.common.domain.enums.tiers import PlatformFeature, PlatformRate
from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class TenantTierPrice(AggregateRoot):
    amount: Decimal
    currency_code: CurrencyCode
    recurrence_interval: TimePeriod

    @property
    def to_dict(self) -> dict:
        return {
            'amount': str(self.amount),
            'currency_code': str(self.currency_code),
            'recurrence_interval': str(self.recurrence_interval),
        }


@dataclass
class TierFeature(AggregateRoot):
    label: PlatformFeature
    is_enabled: bool

    @property
    def to_dict(self) -> dict:
        return {
            'label': str(self.label),
            'is_enabled': self.is_enabled,
        }


@dataclass
class TierRate(AggregateRoot):
    label: PlatformRate
    value: int

    @property
    def to_dict(self) -> dict:
        return {
            'label': str(self.label),
            'value': self.value,
        }

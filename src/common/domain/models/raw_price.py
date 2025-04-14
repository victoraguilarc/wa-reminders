from dataclasses import dataclass
from decimal import Decimal

from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.interfaces.entities import AggregateRoot


@dataclass
class RawPrice(AggregateRoot):
    amount: Decimal
    currency_code: CurrencyCode

    @property
    def to_dict(self) -> dict:
        return {
            'amount': self.amount,
            'currency_code': self.currency_code,
        }

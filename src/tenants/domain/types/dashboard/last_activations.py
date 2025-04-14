from dataclasses import dataclass
from typing import List

from src.tenants.domain.types.dashboard.tenant_activation import TenantActivation


@dataclass
class LastActivations(object):
    month_quantity: int
    activations: List[TenantActivation]

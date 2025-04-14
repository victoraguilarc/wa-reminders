# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.common.domain.enums.growth import TenantLeadChannel, TenantLeadStage
from src.common.domain.interfaces.entities import AggregateRoot
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantId, TenantCustomerLeadId, TenantCustomerLeadAttemptId


@dataclass
class TenantCustomerLeadAttempt(AggregateRoot):
    id: TenantCustomerLeadAttemptId
    attempted_at: datetime


@dataclass
class TenantCustomerLead(AggregateRoot):
    id: TenantCustomerLeadId
    tenant_id: TenantId
    tenant_customer: TenantCustomer
    stage: TenantLeadStage
    channel: Optional[TenantLeadChannel] = None
    attempts: List[TenantCustomerLeadAttempt] = None
    attempted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.attempts = self.attempts or []

    def __eq__(self, other: 'TenantCustomerLead'):
        return self.id == other.id

    def overload(
        self,
        new_instance: 'TenantCustomerLead',
        properties: List[str] = None,
    ):
        instance_properties = properties or self.get_overload_properties()
        for _property in instance_properties:
            if not hasattr(self, _property):
                continue
            property_value = getattr(new_instance, _property)
            setattr(self, _property, property_value)
        return self

    @classmethod
    def get_overload_properties(cls) -> List[str]:
        return [
            'stage',
            'channel',
        ]

    @property
    def to_simple_person(self) -> SimplePerson:
        return self.tenant_customer.to_simple_person

    @property
    def to_persist_dict(self) -> dict:
        return {
            'tenant_id': str(self.tenant_id),
            'tenant_customer_id': str(self.tenant_customer.id),
            'channel': str(self.channel) if self.channel else None,
            'stage': str(self.stage),
        }

    @property
    def to_simple_dict(self) -> dict:
        return {
            'id': str(self.id),
            **self.to_persist_dict,
        }

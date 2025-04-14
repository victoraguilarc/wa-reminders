# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.notifications.enums import NotificationTargetType


@dataclass
class NotificationTarget(object):
    id: UUID
    type: NotificationTargetType

    @property
    def to_dict(self):
        return {
            'id': str(self.id),
            'type': str(self.type),
        }

    @classmethod
    def from_dict(cls, instance_data: dict) -> 'NotificationTarget':
        instance_id = instance_data.get('id')
        return cls(
            id=(UUID(instance_id) if isinstance(instance_id, str) else instance_id),
            type=NotificationTargetType.from_value(instance_data.get('type')),
        )

    @classmethod
    def from_list(cls, instances_data: List[dict]) -> List['NotificationTarget']:
        return [cls.from_dict(instance_data) for instance_data in instances_data]

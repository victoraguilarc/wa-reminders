# -*- coding: utf-8 -*-

from typing import List

from src.common.domain import BaseEnum


class NotificationStatus(BaseEnum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    SENT = 'SENT'


class NotificationTargetType(BaseEnum):
    CLASS = 'CLASS'
    CLASS_STUDENT = 'CLASS_STUDENT'
    GROUP = 'GROUP'


class NotificationStrategy(BaseEnum):
    EMAIL = 'EMAIL'
    SMS = 'SMS'
    WHATSAPP = 'WHATSAPP'
    PUSH_NOTIFICATION = 'PUSH_NOTIFICATION'

    @classmethod
    def from_list(cls, items: List[str]) -> List["NotificationStrategy"]:
        return [cls.from_value(item) for item in items]

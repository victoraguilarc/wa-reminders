# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime

from src.common.domain.enums.notifications import NotificationTemplateCategory
from src.common.domain.value_objects import NotificationTemplateId


@dataclass
class NotificationTemplate(object):
    id: NotificationTemplateId
    html_content: str
    category: NotificationTemplateCategory
    is_active: bool
    created_at: datetime


@dataclass
class RenderedNotification(object):
    category: str
    content: str

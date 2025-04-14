# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.notifications.application.presenters import (
    NotificationPresenter,
    RenderedNotificationPresenter,
)
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_template import RenderedNotification


@dataclass
class NotificationResponse(ApiResponse):
    instance: Notification

    def render(self, locale_context: LocaleContext) -> dict:
        return NotificationPresenter(
            instance=self.instance,
            include_recipients=True,
            locale_context=locale_context,
        ).to_dict


@dataclass
class RenderedNotificationResponse(ApiResponse):
    instance: RenderedNotification

    def render(self, locale_context: LocaleContext) -> dict:
        return RenderedNotificationPresenter(
            instance=self.instance,
            locale_context=locale_context,
        ).to_dict


@dataclass
class NotificationsResponse(ApiResponse):
    instances: List[Notification]

    def render(self, locale_context: LocaleContext) -> List[dict]:
        return [
            NotificationPresenter(
                instance=instance,
                locale_context=locale_context,
            ).to_dict
            for instance in self.instances
        ]

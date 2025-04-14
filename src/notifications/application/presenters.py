# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from src.common.domain.context.locale import LocaleContext
from src.common.helpers.time import TimeUtils
from src.notifications.domain.notification import Notification
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_template import RenderedNotification


@dataclass
class NotificationPresenter(object):
    instance: Notification
    locale_context: LocaleContext
    include_recipients: bool = False

    @property
    def to_dict(self):
        dict_data = {
            'id': str(self.instance.id),
            'subject': self.instance.subject,
            'message': self.instance.message,
            'status': str(self.instance.status),
            'strategies': [str(strategy) for strategy in self.instance.strategies],
            'created_at': TimeUtils.localize_isoformat(self.instance.created_at),
        }

        if not self.include_recipients:
            dict_data['recipients_count'] = self.instance.recipients_count
        else:
            dict_data['recipients'] = [
                NotificationRecipientPresenter(recipient=recipient).to_dict
                for recipient in self.instance.recipients
            ]
        return dict_data


@dataclass
class NotificationRecipientPresenter(object):
    recipient: NotificationRecipient

    @property
    def to_dict(self):
        return {
            'id': str(self.recipient.id),
            'full_name': self.recipient.full_name,
            'email': self.recipient.email,
            'phone_nuber': (
                self.recipient.phone_number.display_phone if self.recipient.phone_number else None
            ),
            'photo_url': self.recipient.photo_url,
        }


@dataclass
class RenderedNotificationPresenter(object):
    instance: Optional[RenderedNotification]
    locale_context: LocaleContext

    @property
    def to_dict(self):
        return {
            'subject': self.locale_context.locale_service.get(
                label='PAYMENT_REMINDER',
                language=self.locale_context.language,
            ),
            'message': self.instance.content,
        }

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.common.domain.value_objects import NotificationId
from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget
from src.notifications.enums import NotificationStatus, NotificationStrategy


@dataclass
class Notification(object):
    id: NotificationId
    subject: str
    message: str
    strategies: List[NotificationStrategy]
    created_at: datetime
    status: NotificationStatus
    targets: List[NotificationTarget]
    html_message: Optional[str] = None
    recipients_count: Optional[int] = None
    recipients: List[NotificationRecipient] = None

    def __post_init__(self):
        self.recipients = self.recipients or []
        self.recipients_count = self.recipients_count or len(self.recipients)

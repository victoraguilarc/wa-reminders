from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.entities.reminder import Reminder, ReminderRecipient


@dataclass
class ReminderRecipientPresenter(object):
    instance: ReminderRecipient

    @property
    def to_dict(self):
        return {
            "id": self.instance.id,
            "phone_number": self.instance.phone_number.to_minimal_dict,
            "status": str(self.instance.status),
        }


@dataclass
class ReminderPresenter(object):
    instance: Reminder
    locale_context: LocaleContext

    @property
    def to_dict(self):
        return {
            "id": self.instance.id,
            "content": self.instance.content,
            "scheduled_time": self.instance.scheduled_time.isoformat(),
            "status": str(self.instance.status),
            "recipients": [
                ReminderRecipientPresenter(instance=recipient).to_dict
                for recipient in self.instance.recipients
            ],
        }

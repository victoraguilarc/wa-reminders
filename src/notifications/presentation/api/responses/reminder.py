from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.entities.reminder import Reminder
from src.notifications.presentation.api.presenters.reminder import ReminderPresenter


@dataclass
class ReminderResponse(object):
    instance: Reminder

    def render(self, locale_context: LocaleContext):
        return ReminderPresenter(self.instance, locale_context).to_dict


@dataclass
class RemindersResponse(object):
    instances: list[Reminder]

    def render(self, locale_context: LocaleContext):
        return [
            ReminderPresenter(instance, locale_context).to_dict
            for instance in self.instances
        ]

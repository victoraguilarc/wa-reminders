# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.application.presenters.pending_action import PendingActionPresenter
from src.common.domain.context.locale import LocaleContext
from src.common.domain.interfaces.responses import ApiResponse
from src.common.domain.models.pending_action import PendingAction


@dataclass
class PendingActionResponse(ApiResponse):
    instance: PendingAction

    def render(self, locale_context: LocaleContext) -> dict:
        return PendingActionPresenter(self.instance).to_dict


@dataclass
class KeyValueResponse(ApiResponse):
    key: str
    value: str

    def render(self, locale_context: LocaleContext) -> dict:
        return {
            self.key: self.value,
        }

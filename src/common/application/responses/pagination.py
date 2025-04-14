# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any

from src.common.domain.context.locale import LocaleContext
from src.common.domain.models.pagination import Page
from src.common.domain.interfaces.responses import ApiResponse


@dataclass
class PaginationResponse(ApiResponse):
    instance: Page
    presenter_class: Any

    def render(self, locale_context: LocaleContext) -> dict:
        return {
            'pagination': self.instance.to_pagination_dict,
            'data': [
                self.presenter_class(item, locale_context).to_dict for item in self.instance.items
            ],
        }

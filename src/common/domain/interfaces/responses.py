# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from src.common.domain.context.locale import LocaleContext


class ApiResponse(ABC):
    @abstractmethod
    def render(self, locale_context: LocaleContext) -> Union[Dict, List, str]:
        raise NotImplementedError


@dataclass
class Presenter(ABC):
    instance: Any

    @property
    def to_dict(self) -> dict:
        raise NotImplementedError

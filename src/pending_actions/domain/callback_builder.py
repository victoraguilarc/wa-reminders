# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CallbackBuilder(ABC):
    hostname: str

    @abstractmethod
    def build_with_token(self, token: str) -> str:
        raise NotImplementedError

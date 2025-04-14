# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from src.common.domain.interfaces.responses import ApiResponse


class UseCase(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


class ApiService(UseCase):
    @abstractmethod
    def execute(self, *args, **kwargs) -> ApiResponse:
        raise NotImplementedError

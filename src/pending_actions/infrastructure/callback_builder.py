# -*- coding: utf-8 -*-

from dataclasses import dataclass

from django.urls import reverse

from src.pending_actions.domain.callback_builder import CallbackBuilder


@dataclass
class DjangoCallbackBuilder(CallbackBuilder):
    view_name: str

    def build_with_token(self, token: str) -> str:
        return '{hostname}{path}'.format(
            hostname=self.hostname,
            path=reverse(self.view_name, kwargs={'token': token}),
        )


@dataclass
class PathCallbackBuilder(CallbackBuilder):
    hostname: str

    def build_with_token(self, token: str) -> str:
        return f'{self.hostname}/{token}'


@dataclass
class QueryParamsCallbackBuilder(CallbackBuilder):
    hostname: str

    def build_with_token(self, token: str) -> str:
        return f'{self.hostname}?token={token}'

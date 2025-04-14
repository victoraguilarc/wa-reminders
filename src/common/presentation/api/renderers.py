# -*- coding: utf-8 -*-

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import renderers

from src.common.helpers.string import is_empty_data
from src.common.helpers.time import TimeUtils


class StandarJSONRenderer(CamelCaseJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']

        if self._is_no_content_response(data, response):
            return super().render(None, accepted_media_type, renderer_context)

        if self._is_paginated_response(data):
            return super().render(data, accepted_media_type, renderer_context)

        if self._is_detail_response(data, response):
            data = {'data': data, 'datetime': str(TimeUtils.utc_now())}

        return super().render(data, accepted_media_type, renderer_context)

    @classmethod
    def _is_no_content_response(cls, data: dict | list, response):
        return is_empty_data(data) and response.status_code == 204

    @classmethod
    def _is_paginated_response(cls, data: dict | list):
        return isinstance(data, dict) and data.get('pagination') is not None

    @classmethod
    def _is_detail_response(cls, data: dict | list, response):
        has_no_exception = response.exception is False
        is_response_covered = isinstance(data, dict) or isinstance(data, list)
        return has_no_exception and is_response_covered


class ZipRenderer(renderers.BaseRenderer):
    media_type = 'application/zip'
    format = 'zip'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

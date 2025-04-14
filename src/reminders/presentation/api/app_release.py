# -*- coding: utf-8 -*-

from constance import config
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.common.presentation.api import DomainAPIView


class AppReleaseView(DomainAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response({
            'version_name': config.APP_RELEASE_VERSION_NAME,
            'version_code': config.APP_RELEASE_VERSION_CODE,
            'is_mandatory': config.APP_RELEASE_MANDATORY,
        })


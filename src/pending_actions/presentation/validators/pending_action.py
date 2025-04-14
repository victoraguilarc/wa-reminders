# -*- coding: utf-8 -*-

from rest_framework import serializers


class PendingActionRequestValidator(serializers.Serializer):
    callback_hostname = serializers.URLField(required=False, allow_null=True)


class PendingActionTokenValidator(serializers.Serializer):
    token = serializers.CharField()


# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.presentation.api.exceptions.base import SerializerFieldExceptionMixin


class EmailAddressValidator(
    SerializerFieldExceptionMixin,
    serializers.Serializer,
):
    email = serializers.EmailField(
        required=False,
        allow_null=True,
    )

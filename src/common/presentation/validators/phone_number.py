# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.presentation.api.exceptions.base import SerializerFieldExceptionMixin


class PhoneNumberValidator(
    SerializerFieldExceptionMixin,
    serializers.Serializer,
):
    dial_code = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=50)
    prefix = serializers.CharField(
        max_length=2,
        required=False,
        allow_null=True,
    )

    # def validate(self, data):
    #     country_config = CountryConfigBuilder.from_dial_code(
    #         dial_code=int(data['dial_code']),
    #     )
    #     try:
    #         raw_phone_number = phonenumbers.parse(
    #             number=data['phone_number'],
    #             region=str(country_config.iso_code),
    #         )
    #     except NumberParseException:
    #         raw_phone_number = None
    #         self.raise_exception(INVALID_PHONE_NUMBER)
    #
    #     is_valid_phone_number = (
    #         bool(raw_phone_number)
    #         and phonenumbers.is_valid_number(raw_phone_number)
    #         and country_config.dial_code == raw_phone_number.country_code
    #     )
    #     if not is_valid_phone_number:
    #         self.raise_exception(INVALID_PHONE_NUMBER)
    #     return data

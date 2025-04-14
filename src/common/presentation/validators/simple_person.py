# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.presentation.validators.phone_number import PhoneNumberValidator


class OptionalPersonValidator(serializers.Serializer):
    first_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    paternal_surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    maternal_surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )


class SimplePersonValidator(serializers.Serializer):
    first_name = serializers.CharField()
    paternal_surname = serializers.CharField()
    maternal_surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_null=True,
    )
    phone_number = PhoneNumberValidator(
        required=False,
        allow_null=True,
    )

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError(
                'Either email or phone is required',
            )
        return data


class LeadSimplePersonValidator(serializers.Serializer):
    first_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    paternal_surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    maternal_surname = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_null=True,
    )
    phone_number = PhoneNumberValidator(
        required=False,
        allow_null=True,
    )

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError(
                'Either email or phone is required',
            )
        return data


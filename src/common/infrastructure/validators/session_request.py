# -*- coding: utf-8 -*-

from rest_framework import serializers


class EmailLoginValidator(serializers.Serializer):
    email = serializers.EmailField()


class WhatsappLoginValidator(serializers.Serializer):
    dial_code = serializers.IntegerField()
    phone_number = serializers.CharField()

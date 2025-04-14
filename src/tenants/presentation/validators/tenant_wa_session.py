# -*- coding: utf-8 -*-


from rest_framework import serializers

from src.common.domain.enums.tenants import WhatsappSessionStatus


class UpdateTenantWhatsappSessionValidator(serializers.Serializer):
    enabled = serializers.BooleanField(required=False)



class WhatsappSessionStatusValidator(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.ChoiceField(choices=WhatsappSessionStatus.choices())


class WhatsappSessionStatusPayloadValidator(serializers.Serializer):
    payload = WhatsappSessionStatusValidator(required=True)


class WhatsappSessionPatchValidator(serializers.Serializer):
    messaging_enabled = serializers.BooleanField(required=False)
    agents_enabled = serializers.BooleanField(required=False)

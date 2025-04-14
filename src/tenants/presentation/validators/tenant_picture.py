# -*- coding: utf-8 -*-


from rest_framework import serializers

from src.common.domain.enums.tenants import TenantPictureCategory


class CreateTenantPictureValidator(serializers.Serializer):
    image = serializers.ImageField(required=True, allow_null=False)
    category = serializers.ChoiceField(
        choices=TenantPictureCategory.choices(),
        required=False,
    )

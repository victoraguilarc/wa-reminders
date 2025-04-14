# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer

from src.common.constants import DEFAULT_LANGUAGE
from src.common.database.models import TenantUserORM
from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import TenantUserStatus
from src.common.presentation.api.exceptions.base import BaseModelSerializer
from src.common.presentation.api.rest_fields import Base64ImageField
from src.common.presentation.validators.phone_number import PhoneNumberValidator
from src.users.presentation.validators.email_address import EmailAddressValidator

common_fields = (
    'tenant_role_id',
    'email_address',
    'phone_number',
    'first_name',
    'paternal_surname',
    'maternal_surname',
    'photo',
    'status',
    'lang',
)

class TenantUserValidator(BaseModelSerializer):
    tenant_role_id = serializers.UUIDField(required=False)
    email_address = EmailAddressValidator(required=False, allow_null=True)
    phone_number = PhoneNumberValidator(
        required=False,
        allow_null=True,
    )
    photo = Base64ImageField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        required=False,
        choices=TenantUserStatus.choices(),
    )
    lang = serializers.ChoiceField(
        required=False,
        choices=Language.choices(),
        default=str(DEFAULT_LANGUAGE),
    )

    class Meta:
        model = TenantUserORM
        fields = common_fields


class TenantUserPasswordValidator(Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()


class CreateTenantUserValidator(Serializer):
    tenant_user = TenantUserValidator()
    send_invitation = serializers.BooleanField(
        required=False,
        default=False,
    )

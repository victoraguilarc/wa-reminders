# -*- coding: utf-8 -*-

from rest_framework import serializers

from src.common.constants import DEFAULT_LANGUAGE
from src.common.database.models import TenantCustomerORM
from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import TenantCustomerStatus, TenantCustomerCreationSource
from src.common.presentation.api.exceptions.base import BaseModelSerializer
from src.common.presentation.api.rest_fields import Base64ImageField
from src.common.presentation.validators.phone_number import PhoneNumberValidator
from src.users.presentation.validators.email_address import EmailAddressValidator

common_fields = (
    'email_address',
    'first_name',
    'paternal_surname',
    'maternal_surname',
    'birth_date',
    'photo',
    'lang',
    'phone_number',
    'gender',
    'status',
    'creation_source',
)


class TenantCustomerValidator(BaseModelSerializer):
    email_address = EmailAddressValidator(required=False, allow_null=True)
    phone_number = PhoneNumberValidator(
        required=False,
        allow_null=True,
    )
    photo = Base64ImageField(required=False, allow_null=True)
    lang = serializers.ChoiceField(
        required=False,
        choices=Language.choices(),
        default=str(DEFAULT_LANGUAGE),
    )
    status = serializers.ChoiceField(
        required=False,
        choices=TenantCustomerStatus.choices(),
    )
    creation_source = serializers.ChoiceField(
        required=False,
        choices=TenantCustomerCreationSource.choices(),
    )

    def get_value(self, dictionary):
        return super().get_value(dictionary)

    class Meta:
        model = TenantCustomerORM
        fields = common_fields

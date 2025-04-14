from rest_framework import serializers

from src.common.database.models import TenantORM
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone
from src.common.domain.enums.tenants import LinkedSiteCategory
from src.common.presentation.api.rest_fields import Base64ImageField

common_fields = (
    'name',
    'slug',
    'country_iso_code',
    'logo',
)


class CreateTenantValidator(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_null=True)
    country_iso_code = serializers.ChoiceField(choices=CountryIsoCode.choices())
    logo = Base64ImageField(required=False, allow_null=False)

    class Meta:
        model = TenantORM
        fields = common_fields


class UpdateTenantValidator(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_null=False)
    slug = serializers.SlugField(required=False, allow_null=True)
    country_iso_code = serializers.ChoiceField(
        choices=CountryIsoCode.choices(),
        required=False,
    )
    currency_code = serializers.ChoiceField(
        choices=CurrencyCode.choices(),
        required=False,
    )
    timezone = serializers.ChoiceField(
        choices=TimeZone.choices(),
        required=False,
    )
    logo = Base64ImageField(required=False, allow_null=False)

    class Meta:
        model = TenantORM
        fields = common_fields + (
            'currency_code',
            'timezone',
        )


class TenantFromSiteValidator(serializers.Serializer):
    domain = serializers.CharField(required=True, allow_null=False)
    category = serializers.ChoiceField(
        choices=LinkedSiteCategory.choices(),
        default=str(LinkedSiteCategory.MEMBERS_SITE),
    )
    include_resources = serializers.BooleanField(
        required=False,
        default=False,
    )


class TenantFromWhatsappSessionValidator(serializers.Serializer):
    session_name = serializers.CharField(required=True, allow_null=False)


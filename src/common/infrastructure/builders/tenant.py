from src.common.database.models import TenantORM
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_container import TenantContainer
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone, Language
from src.common.domain.enums.tenants import TenantStatus
from src.common.domain.value_objects import TenantId, TenantSlug, UserId
from src.common.infrastructure.builders.user import build_user


def build_tenant(orm_instance: TenantORM) -> Tenant:
    return Tenant(
        id=TenantId(orm_instance.uuid),
        name=orm_instance.name,
        slug=TenantSlug(orm_instance.slug),
        timezone=TimeZone.from_value(orm_instance.timezone),
        lang=Language.from_value(orm_instance.lang),
        currency_code=CurrencyCode.from_value(orm_instance.currency_code),
        owner_id=(
            UserId(orm_instance.owner.uuid)
            if orm_instance.owner else None
        ),
        country_iso_code=CountryIsoCode.from_value(orm_instance.country_iso_code),
        grace_period=orm_instance.grace_period,
        checkin_from_in_hours=orm_instance.checkin_from_in_hours,
        checkin_until_in_hours=orm_instance.checkin_until_in_hours,
        reference=orm_instance.reference,
        status=TenantStatus.from_value(orm_instance.status),
        logo_url=orm_instance.logo_url,
        created_at=orm_instance.created_at,
        refresh_expiration_on_passes=orm_instance.refresh_expiration_on_passes,
        membership_changes_with_remaining=orm_instance.membership_changes_with_remaining,
        max_free_trials=orm_instance.max_free_trials,
        num_whatsapp_sessions=orm_instance.num_whatsapp_sessions,
    )


def build_tenant_container(
    orm_instance: TenantORM,
) -> TenantContainer:
    return TenantContainer(
        tenant=build_tenant(orm_instance),
        owner=(
            build_user(orm_instance.owner)
            if orm_instance.owner else None
        ),
    )

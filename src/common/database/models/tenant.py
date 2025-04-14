# -*- coding: utf-8 -*-

from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from src.common.constants import (
    DEFAULT_MEMBERSHIP_PLAN_GRACE_PERIOD_IN_DAYS,
    DEFAULT_LANGUAGE,
    DEFAULT_NUM_WHAPSAPP_SESSIONS, DEFAULT_CHECKIN_FROM_SESSIONS_IN_HOURS, DEFAULT_CHECKIN_UNTIL_SESSIONS_IN_HOURS,
)
from src.common.database.models.mixins.common import UUIDTimestampMixin
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import TimeZone, Language
from src.common.domain.enums.tenants import TenantStatus
from src.common.presentation.utils.files import clean_static_url


def tenants_logos_path(instance, filename):
    return '/'.join(['tenants', 'logos', filename])


class TenantORM(UUIDTimestampMixin):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        'UserORM',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        related_name='owned_organizations',
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=100, unique=True)
    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    country_iso_code = models.CharField(
        choices=CountryIsoCode.choices(),
        default=CountryIsoCode.MEXICO.value,
        max_length=3,
        verbose_name='Country',
    )
    lang = models.CharField(
        verbose_name='Language',
        choices=Language.choices(),
        max_length=3,
        default=str(DEFAULT_LANGUAGE),
    )
    timezone = models.CharField(
        choices=TimeZone.choices(),
        default=TimeZone.MEXICO_CITY.value,
        max_length=255,
        verbose_name='Timezone',
    )
    currency_code = models.CharField(
        verbose_name='Currency',
        max_length=3,
        choices=CurrencyCode.choices(),
        default=CurrencyCode.MXN.value,
    )
    logo = ProcessedImageField(
        verbose_name='Logo',
        upload_to=tenants_logos_path,
        processors=[ResizeToFill(512, 512)],
        format='PNG',
        options={'quality': 80},
        blank=True,
        null=True,
    )

    grace_period = models.PositiveSmallIntegerField(
        verbose_name='Grace Period',
        default=DEFAULT_MEMBERSHIP_PLAN_GRACE_PERIOD_IN_DAYS,
    )
    checkin_from_in_hours = models.PositiveSmallIntegerField(
        verbose_name='Checkin From Hours',
        help_text='Time window to checkin from in hours',
        default=DEFAULT_CHECKIN_FROM_SESSIONS_IN_HOURS,
    )
    checkin_until_in_hours = models.PositiveSmallIntegerField(
        verbose_name='Checkin Until Hours',
        help_text='Time window to checkin until in hours',
        default=DEFAULT_CHECKIN_UNTIL_SESSIONS_IN_HOURS,
    )
    status = models.CharField(
        choices=TenantStatus.choices(),
        max_length=60,
        default=str(TenantStatus.PENDING),
    )
    refresh_expiration_on_passes = models.BooleanField(
        verbose_name='Refresh Expiration on Passes?',
        help_text='If enabled, when a bundle passes membership is renewed, its expiration will be refreshed',
        default=False,
    )
    membership_changes_with_remaining = models.BooleanField(
        verbose_name='Refill passes on changes?',
        help_text='If enabled, when a membership plan is changed in a membership change, its expiration or passes will be refilled with the remaining',
        default=False,
    )
    max_free_trials = models.PositiveSmallIntegerField(
        verbose_name='Max Free Trials',
        help_text='Max number of free trials that a user can have by class',
        default=1,
    )
    days_between_trials = models.PositiveSmallIntegerField(
        verbose_name='Days Between Trials',
        help_text='Max number of days between free trials that a user can have by class',
        default=365,
    )
    num_whatsapp_sessions = models.PositiveSmallIntegerField(
        verbose_name='Max Whatsapp Sessions',
        help_text='Number of WhatsApp Sessions that the tenant has',
        default=DEFAULT_NUM_WHAPSAPP_SESSIONS,
    )

    @property
    def is_active(self):
        return self.status == TenantStatus.ACTIVE.value

    @property
    def display_owner(self):
        return self.owner.email_address if self.owner else "----"

    def __str__(self):
        return str(self.slug)

    @property
    def logo_url(self):
        return clean_static_url(self.logo.url) if self.logo else None

    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

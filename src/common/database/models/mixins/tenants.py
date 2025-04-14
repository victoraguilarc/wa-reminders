from django.db import models

from src.common.database.models.mixins.common import UUIDTimestampMixin


class TenantMixin(models.Model):
    tenant = models.ForeignKey('TenantORM', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UUIDTimestampTenantMixin(TenantMixin, UUIDTimestampMixin):
    """An abstract base class model that provides an uuid and timestamp fields."""

    class Meta:
        abstract = True


class OptionalTenantMixin(models.Model):
    tenant = models.ForeignKey(
        'TenantORM',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class TierMixin(models.Model):
    tier = models.ForeignKey(
        'TierORM',
        verbose_name='Tier',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

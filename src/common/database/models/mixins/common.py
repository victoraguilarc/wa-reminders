# -*- coding: utf-8 -*-

import uuid

from django.db import models

from src.common.database.models.managers.availability import SoftDeleteManager


class TimeStampedModelMixin(models.Model):
    """Timestamp extra field.

    An abstract base class model that provides self updating 'created' and 'modified' fields
    https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class UUIDModelMixin(models.Model):
    """An abstract base class model that provides an uuid field."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    """An abstract base class model that provides a slug field."""

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModelMixin(models.Model):
    """An abstract base class model that provides an uuid field that is the primary key."""

    uuid = models.UUIDField(
        verbose_name='UUID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class UUIDTimestampMixin(UUIDPrimaryKeyModelMixin, TimeStampedModelMixin):
    """An abstract base class model that provides an uuid and timestamp fields."""

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(
        verbose_name='Deleted',
        default=False,
    )

    objects = models.Manager()
    available_objects = SoftDeleteManager()

    @property
    def is_available(self) -> bool:
        return not self.is_deleted

    class Meta:
        abstract = True

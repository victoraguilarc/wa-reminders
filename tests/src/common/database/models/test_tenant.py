# -*- coding: utf-8 -*-

import pytest

from src.common.database.models import TenantORM
from src.common.database.models.factories.tenant import TenantORMFactory


@pytest.mark.django_db
def test_string_representation():
    instance = TenantORMFactory()
    assert str(instance) == str(instance.slug)


def test_verbose_name():
    assert str(TenantORM._meta.verbose_name) == 'Tenant'


def test_verbose_name_plural():
    assert str(TenantORM._meta.verbose_name_plural) == 'Tenants'

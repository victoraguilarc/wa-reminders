# -*- coding: utf-8 -*-

import pytest

from src.common.database.models import TenantTierORM
from src.common.database.models.factories.tenant_tier import TenantTierORMFactory


@pytest.mark.django_db
def test_string_representation():
    instance = TenantTierORMFactory()
    assert str(instance) == f'{instance.uuid}'


def test_verbose_name():
    assert str(TenantTierORM._meta.verbose_name) == 'Tenant Tier'


def test_verbose_name_plural():
    assert str(TenantTierORM._meta.verbose_name_plural) == 'Tenant Tiers'

# -*- coding: utf-8 -*-

import pytest

from src.common.database.models import TenantCustomerORM
from src.common.database.models.factories.tenant_customer import TenantCustomerORMFactory


@pytest.mark.django_db
def test_string_representation_with_email():
    instance: TenantCustomerORM = TenantCustomerORMFactory()
    assert str(instance) == f'{instance.email_address.email}/{instance.tenant}'


@pytest.mark.django_db
def test_string_representation_with_phone_number():
    instance: TenantCustomerORM = TenantCustomerORMFactory(email_address=None)
    assert str(instance) == f'{instance.phone_number.phone_number}/{instance.tenant}'


def test_verbose_name():
    assert str(TenantCustomerORM._meta.verbose_name) == 'Tenant Customer'


def test_verbose_name_plural():
    assert str(TenantCustomerORM._meta.verbose_name_plural) == 'Tenant Customers'

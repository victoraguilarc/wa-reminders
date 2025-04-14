# -*- coding: utf-8 -*-

import factory
from factory.django import DjangoModelFactory

from src.common.database.models import TenantUserORM
from src.common.database.models.factories.tenant import TenantORMFactory
from src.common.database.models.factories.user import UserORMFactory
from src.common.presentation.utils.testing.faker import instance_faker

faker = instance_faker()


class TenantUserORMFactory(DjangoModelFactory):
    user = factory.SubFactory(UserORMFactory)
    tenant = factory.SubFactory(TenantORMFactory)
    first_name = factory.LazyFunction(faker.word)
    paternal_surname = factory.LazyFunction(faker.word)
    maternal_surname = factory.LazyFunction(faker.word)

    class Meta:
        model = TenantUserORM

# -*- coding: utf-8 -*-

import factory

from src.common.database.models import TenantORM
from src.common.database.models.factories.user import UserORMFactory
from src.common.presentation.utils.testing.faker import instance_faker

faker = instance_faker()


class TenantORMFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserORMFactory)
    name = factory.LazyFunction(faker.word)
    slug = factory.LazyFunction(faker.uuid4)

    class Meta:
        model = TenantORM

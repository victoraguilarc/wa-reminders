# -*- coding: utf-8 -*-

import factory
from factory.django import DjangoModelFactory

from src.common.database.models import TenantCustomerORM
from src.common.database.models.factories.email_address import EmailAddressORMFactory
from src.common.database.models.factories.phone_number import PhoneNumberORMFactory
from src.common.database.models.factories.tenant import TenantORMFactory
from src.common.database.models.factories.user import UserORMFactory
from src.common.presentation.utils.testing.faker import instance_faker

faker = instance_faker()


class TenantCustomerORMFactory(DjangoModelFactory):
    user = factory.SubFactory(UserORMFactory)
    tenant = factory.SubFactory(TenantORMFactory)
    email_address = factory.SubFactory(EmailAddressORMFactory)
    phone_number = factory.SubFactory(PhoneNumberORMFactory)

    first_name = factory.LazyFunction(faker.word)
    paternal_surname = factory.LazyFunction(faker.word)
    maternal_surname = factory.LazyFunction(faker.word)


    class Meta:
        model = TenantCustomerORM

# -*- coding: utf-8 -*-
import secrets

import factory

from src.common.database.models import PendingActionORM
from src.common.domain.enums.users import PendingActionCategory
from src.common.helpers import dates
from src.common.presentation.utils.testing.faker import instance_faker

faker = instance_faker()


def now_after_three():
    return dates.ago(days=3)

def random_category() -> str:
    return secrets.choice(PendingActionCategory.values())

class PendingActionORMFactory(factory.django.DjangoModelFactory):
    category =  factory.LazyFunction(random_category)
    expired_at = factory.LazyFunction(now_after_three)
    token = factory.LazyFunction(faker.uuid4)

    class Meta:
        model = PendingActionORM

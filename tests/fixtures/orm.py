from datetime import datetime

import pytest

from src.common.database.models import (
    UserORM,
    TenantORM,
    EmailAddressORM,
    PhoneNumberORM,
)
from src.common.database.models.factories.email_address import EmailAddressORMFactory
from src.common.database.models.factories.pending_action import PendingActionORMFactory
from src.common.database.models.factories.phone_number import PhoneNumberORMFactory
from src.common.database.models.factories.tenant import TenantORMFactory
from src.common.database.models.factories.tenant_customer import TenantCustomerORMFactory
from src.common.database.models.factories.tenant_user import TenantUserORMFactory
from src.common.database.models.factories.user import UserORMFactory
from src.common.domain.enums.countries import CountryIsoCode

TEST_PASSWORD = 'test_password'
TEST_TENANT_SLUG = 'test-tenant'
TEST_EMAIL = 'test@collectives.dev'

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user_orm():
    user = UserORMFactory()
    user.set_password(TEST_PASSWORD)
    user.save()
    return user


@pytest.fixture
def email_address_orm() -> EmailAddressORM:
    return EmailAddressORMFactory(email=TEST_EMAIL)


@pytest.fixture
def phone_number_orm() -> PhoneNumberORM:
    return PhoneNumberORMFactory(
        iso_code=CountryIsoCode.MEXICO,
        dial_code=52,
        phone_number='5544332211',
        is_verified=True,
    )


@pytest.fixture
def tenant_orm():
    return TenantORMFactory(slug=TEST_TENANT_SLUG)


@pytest.fixture
def pending_action_orm():
    return PendingActionORMFactory()


@pytest.fixture
def tenant_customer_orm(
    tenant_orm: TenantORM,
    user_orm: UserORM,
    email_address_orm: EmailAddressORM,
    phone_number_orm: PhoneNumberORM,
):
    return TenantCustomerORMFactory(
        tenant=tenant_orm,
        user=user_orm,
        email_address=email_address_orm,
        phone_number=phone_number_orm,
    )



@pytest.fixture
def tenant_user_orm(tenant_orm, user_orm):
    return TenantUserORMFactory(tenant=tenant_orm, user=user_orm)



@pytest.fixture
def extra_tenant_orm():
    return TenantORMFactory()


@pytest.fixture
def extra_tenant_customer_orm(extra_tenant_orm):
    return TenantCustomerORMFactory(tenant=extra_tenant_orm)


@pytest.fixture
def extra_tenant_user_orm(extra_tenant_orm):
    return TenantUserORMFactory(tenant=extra_tenant_orm)


@pytest.fixture(scope='function')
def ocurrence() -> datetime:
    return datetime(year=2024, month=6, day=1, hour=0, minute=0, second=0, microsecond=0)


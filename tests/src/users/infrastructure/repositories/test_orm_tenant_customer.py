from uuid import uuid4

import pytest
from expects import be_a, be_none, equal, expect

from src.common.database.models import PhoneNumberORM, TenantORM, TenantCustomerORM, EmailAddressORM
from src.common.database.models.factories.phone_number import PhoneNumberORMFactory
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.users import TenantCustomerStatus
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.user import User
from src.common.domain.value_objects import (
    EmailAddressId,
    PhoneNumberId,
    RawPhoneNumber,
    TenantCustomerId, TenantId,
)
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.users.infrastructure.repositories import ORMTenantCustomerRepository

pytestmark = [pytest.mark.django_db]


@pytest.fixture(scope='function')
def repository():
    return ORMTenantCustomerRepository()


@pytest.fixture(scope='function')
def simple_person() -> SimplePerson:
    return SimplePerson(
        first_name='John',
        paternal_surname='Doe',
        maternal_surname='Unknown',
    )


def test_create_from_simple_person(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
):
    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=None,
        status=TenantCustomerStatus.INACTIVE,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.INACTIVE))
    expect(tenant_customer.user).to(be_a(User))
    expect(tenant_customer.email_address).to(be_none)
    expect(tenant_customer.phone_number).to(be_none)


def test_create_from_simple_person_with_email(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
):
    simple_person.email = 'mail@example.com'

    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=None,
        status=TenantCustomerStatus.INACTIVE,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.INACTIVE))
    expect(tenant_customer.user).to(be_a(User))
    expect(tenant_customer.email_address).to(be_a(EmailAddress))
    expect(tenant_customer.email_address.email).to(equal(simple_person.email))
    expect(tenant_customer.phone_number).to(be_none)


def test_create_from_simple_person_with_existent_email(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
    email_address_orm: EmailAddressORM,
):
    simple_person.email = email_address_orm.email

    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=None,
        status=TenantCustomerStatus.INACTIVE,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.INACTIVE))
    expect(tenant_customer.user).to(be_a(User))
    expect(tenant_customer.email_address).to(be_a(EmailAddress))
    expect(tenant_customer.email_address.email).to(equal(simple_person.email))
    expect(tenant_customer.email_address.id).to(equal(EmailAddressId(email_address_orm.uuid)))
    expect(tenant_customer.phone_number).to(be_none)


def test_create_from_simple_person_with_existent_phone_number(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
):
    phone_number_orm: PhoneNumberORM = PhoneNumberORMFactory()
    simple_person.phone_number = RawPhoneNumber(
        iso_code=CountryIsoCode.from_value(phone_number_orm.iso_code),
        dial_code=phone_number_orm.dial_code,
        phone_number=phone_number_orm.phone_number,
        prefix=phone_number_orm.prefix,
    )

    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=None,
        status=TenantCustomerStatus.INACTIVE,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.INACTIVE))
    expect(tenant_customer.user).to(be_a(User))
    expect(tenant_customer.email_address).to(be_none)
    expect(tenant_customer.phone_number).to(be_a(PhoneNumber))
    expect(tenant_customer.phone_number.id).to(equal(PhoneNumberId(phone_number_orm.uuid)))


def test_create_from_simple_person_with_email_and_phone_number(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
):
    simple_person.phone_number = RawPhoneNumber(
        iso_code=CountryIsoCode.MEXICO,
        dial_code=52,
        phone_number='1234567890',
        prefix='1',
    )

    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=None,
        status=TenantCustomerStatus.INACTIVE,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.INACTIVE))
    expect(tenant_customer.user).to(be_a(User))
    expect(tenant_customer.email_address).to(be_none)
    expect(tenant_customer.phone_number).to(be_a(PhoneNumber))
    expect(tenant_customer.phone_number.phone_number).to(
        equal(simple_person.phone_number.phone_number)
    )
    expect(tenant_customer.phone_number.dial_code).to(equal(simple_person.phone_number.dial_code))
    expect(tenant_customer.phone_number.iso_code).to(equal(simple_person.phone_number.iso_code))
    expect(tenant_customer.phone_number.prefix).to(equal(simple_person.phone_number.prefix))


def test_create_from_simple_person_with_custom_uuid(
    tenant_orm: TenantORM,
    repository: ORMTenantCustomerRepository,
    simple_person: SimplePerson,
):
    tenant_customer_id = TenantCustomerId(uuid4())

    tenant_customer = repository.get_or_create_from_person(
        tenant_id=tenant_orm.uuid,
        person=simple_person,
        tenant_customer_id=tenant_customer_id,
    )

    expect(tenant_customer).to(be_a(TenantCustomer))
    expect(tenant_customer.status).to(equal(TenantCustomerStatus.ACTIVE))
    expect(tenant_customer.id).to(equal(tenant_customer_id))


def test_find_for_session_by_email(
    tenant_customer_orm: TenantCustomerORM,
    repository: ORMTenantCustomerRepository,
):
    result_orm = repository.find_for_session(
        tenant_id=TenantId(tenant_customer_orm.tenant_id),
        email=tenant_customer_orm.email_address.email,
    )

    expect(result_orm).to(be_a(TenantCustomer))
    expect(result_orm.id).to(
        equal(TenantCustomerId(tenant_customer_orm.uuid)),
    )


def test_find_for_session_by_email_and_raw_phone_number(
    tenant_customer_orm: TenantCustomerORM,
    repository: ORMTenantCustomerRepository,
):
    phone_number = build_phone_number(tenant_customer_orm.phone_number)

    result_orm = repository.find_for_session(
        tenant_id=TenantId(tenant_customer_orm.tenant_id),
        email=tenant_customer_orm.email_address.email,
        raw_phone_number=phone_number.raw_phone_number,
    )

    expect(result_orm).to(be_a(TenantCustomer))
    expect(result_orm.id).to(
        equal(TenantCustomerId(tenant_customer_orm.uuid)),
    )

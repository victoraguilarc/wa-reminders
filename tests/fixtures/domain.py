import uuid

import pytest
from src.common.domain.enums.class_sessions import (
    SessionAttendeeStatus,
    CustomerCheckinCategory,
    TenantClassSessionPassStatus,
)
from src.common.domain.enums.payments import PaymentMode, PaymentTaxBehavior
from src.common.domain.enums.tenant_classes import TenantClassStatus

from src.common.domain.context.locale import LocaleContext
from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.enums.currencies import CurrencyCode
from src.common.domain.enums.locales import Language, TimeZone
from src.common.domain.enums.tenants import TenantStatus
from src.common.domain.enums.users import (
    TenantCustomerStatus,
    TenantCustomerCreationSource,
    PendingActionCategory,
    PendingActionStatus, TenantUserStatus,
)
from src.common.domain.interfaces.faker import FakerInterface
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.models.user import User
from src.common.domain.value_objects import (
    UserId,
    TenantId,
    TenantSlug,
    EmailAddressId,
    PhoneNumberId,
    TenantClassId,
    PendingActionId, RawPhoneNumber,
)


@pytest.fixture
def tenant(
    faker: FakerInterface,
) -> Tenant:
    return Tenant(
        id=TenantId(uuid.uuid4()),
        name=faker.word(),
        owner_id=UserId(faker.uuid4()),
        slug=TenantSlug(faker.uuid4()),
        status=TenantStatus.ACTIVE,
        timezone=TimeZone.UTC,
        lang=Language.ES,
        currency_code=CurrencyCode.MXN,
        country_iso_code=CountryIsoCode.MEXICO,
    )

@pytest.fixture(scope='function')
def raw_phone_number() -> RawPhoneNumber:
    return RawPhoneNumber(
        iso_code=CountryIsoCode.MEXICO,
        dial_code=52,
        phone_number='5544332211',
        prefix=None,
    )


@pytest.fixture
def phone_number(
    raw_phone_number: RawPhoneNumber,
) -> PhoneNumber:
    return PhoneNumber(
        id=PhoneNumberId(uuid.uuid4()),
        iso_code=raw_phone_number.iso_code,
        dial_code=raw_phone_number.dial_code,
        phone_number=raw_phone_number.phone_number,
        prefix=raw_phone_number.prefix,
        is_verified=False,
    )


@pytest.fixture
def email_address() -> EmailAddress:
    return EmailAddress(
        id=EmailAddressId(uuid.uuid4()),
        email='test@collectives.pro',
        is_verified=True,
    )


@pytest.fixture
def another_phone_number() -> PhoneNumber:
    return PhoneNumber(
        id=PhoneNumberId(uuid.uuid4()),
        iso_code=CountryIsoCode.MEXICO,
        dial_code=52,
        phone_number='5543211234',
        is_verified=True,
        prefix=None,
    )


@pytest.fixture
def another_email_address() -> EmailAddress:
    return EmailAddress(
        id=EmailAddressId(uuid.uuid4()),
        email='qa@collectives.pro',
        is_verified=True,
    )


@pytest.fixture
def user(
    phone_number: PhoneNumber,
    email_address: EmailAddress,
) -> User:
    return User(
        id=UserId(uuid.uuid4()),
        email_address=email_address,
        phone_number=phone_number,
    )


@pytest.fixture
def simple_person(
    faker: FakerInterface,
) -> SimplePerson:
    return SimplePerson(
        first_name=faker.first_name(),
        paternal_surname=faker.last_name(),
        maternal_surname=faker.first_name(),
        email=faker.email(),
    )


@pytest.fixture
def another_user(
    another_phone_number: PhoneNumber,
    another_email_address: EmailAddress,
) -> User:
    return User(
        id=UserId(uuid.uuid4()),
        email_address=another_email_address,
        phone_number=another_phone_number,
    )


@pytest.fixture
def pending_action(
    user: User,
    faker: FakerInterface
) -> PendingAction:
    return PendingAction(
        id=PendingActionId(uuid.uuid4()),
        category=PendingActionCategory.EMAIL_ADDRESS_VERIFICATION,
        status=PendingActionStatus.PENDING,
        token=faker.uuid4(),
        tracking_code=faker.uuid4(),
        metadata={},
    )


@pytest.fixture
def payment_mode() -> PaymentMode:
    return PaymentMode.ONE_TIME


@pytest.fixture
def tenant_customer(
    user: User,
    tenant: Tenant,
    phone_number: PhoneNumber,
    email_address: EmailAddress,
):
    return TenantCustomer(
        id=TenantClassId(uuid.uuid4()),
        tenant_id=tenant.id,
        user=user,
        status=TenantCustomerStatus.ACTIVE,
        creation_source=TenantCustomerCreationSource.UNDEFINED,
        email_address=email_address,
        phone_number=phone_number,
        first_name='Fulanito',
        paternal_surname='de Tal',
        maternal_surname=None,
        lang=Language.ES,
        photo_url=None,
        photo=None,
        birth_date=None,
        gender=None,
    )


@pytest.fixture
def tenant_user(
    user: User,
    tenant: Tenant,
    phone_number: PhoneNumber,
    email_address: EmailAddress,
):
    return TenantUser(
        id=TenantClassId(uuid.uuid4()),
        tenant_id=tenant.id,
        user=user,
        status=TenantUserStatus.ACTIVE,
        first_name='Fulanito',
        paternal_surname='de Tal',
        maternal_surname=None,
        lang=Language.ES,
        photo_url=None,
        photo=None,
        birth_date=None,
        gender=None,
        is_owner=False,
    )

@pytest.fixture
def another_tenant_customer(
    another_user: User,
    tenant: Tenant,
    another_phone_number: PhoneNumber,
    another_email_address: EmailAddress,
):
    return TenantCustomer(
        id=TenantClassId(uuid.uuid4()),
        tenant_id=tenant.id,
        user=another_user,
        email_address=another_email_address,
        phone_number=another_phone_number,
        status=TenantCustomerStatus.ACTIVE,
        creation_source=TenantCustomerCreationSource.UNDEFINED,
        first_name='Juanito',
        paternal_surname='Perez',
        maternal_surname=None,
        lang=Language.ES,
        photo_url=None,
        photo=None,
        birth_date=None,
        gender=None,
    )


@pytest.fixture
def locale_context() -> LocaleContext:
    return LocaleContext(
        time_zone=TimeZone.UTC,
        language=Language.ES,
        country_config=CountryConfigBuilder.from_iso_code(
            iso_code=CountryIsoCode.MEXICO,
        ),
    )

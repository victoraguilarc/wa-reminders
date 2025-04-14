from src.common.database.models import TenantCustomerORM
from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import Gender, TenantCustomerStatus, TenantCustomerCreationSource
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.common.infrastructure.builders.email_address import build_email_address
from src.common.infrastructure.builders.phone_number import build_phone_number
from src.common.infrastructure.builders.user import build_user


def build_tenant_customer(
    orm_instance: TenantCustomerORM,
    has_memberships: bool = False,
) -> TenantCustomer:
    return TenantCustomer(
        id=TenantCustomerId(orm_instance.uuid),
        tenant_id=TenantId(orm_instance.tenant_id),
        user=build_user(orm_instance.user),
        email_address=(
            build_email_address(orm_instance.email_address) if orm_instance.email_address else None
        ),
        phone_number=(
            build_phone_number(orm_instance.phone_number) if orm_instance.phone_number else None
        ),
        status=TenantCustomerStatus.from_value(orm_instance.status),
        creation_source=TenantCustomerCreationSource.from_value(orm_instance.creation_source),
        lang=Language.from_value(orm_instance.lang),
        first_name=orm_instance.first_name,
        paternal_surname=orm_instance.paternal_surname,
        maternal_surname=orm_instance.maternal_surname,
        birth_date=orm_instance.birth_date,
        gender=(Gender.from_value(orm_instance.gender) if orm_instance.gender else None),
        photo=None,
        photo_url=orm_instance.photo_url,
        created_at=orm_instance.created_at,
        has_memberships=has_memberships,
    )

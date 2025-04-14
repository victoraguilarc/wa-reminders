from src.common.database.models.tenant_user import TenantUserORM
from src.common.domain.enums.locales import Language
from src.common.domain.enums.users import TenantUserStatus, Gender
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import TenantCustomerId, TenantId
from src.common.infrastructure.builders.user import build_user


def build_tenant_user(orm_instance: TenantUserORM) -> TenantUser:
    return TenantUser(
        id=TenantCustomerId(orm_instance.uuid),
        tenant_id=TenantId(orm_instance.tenant.uuid),
        user=build_user(orm_instance.user),
        status=TenantUserStatus.from_value(orm_instance.status),
        lang=Language.from_value(orm_instance.lang),
        first_name=orm_instance.first_name,
        paternal_surname=orm_instance.paternal_surname,
        maternal_surname=orm_instance.maternal_surname,
        created_at=orm_instance.created_at,
        photo_url=orm_instance.photo_url,
        birth_date=orm_instance.birth_date,
        gender=(
            Gender.from_value(orm_instance.gender)
            if orm_instance.gender else None
        ),
        is_owner=orm_instance.is_owner,
        photo=None,
    )

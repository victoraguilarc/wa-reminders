# -*- coding: utf-8 -*-

from src.common.database.models import TenantPictureORM
from src.common.domain.entities.tenant_picture import TenantPicture
from src.common.domain.enums.tenants import TenantPictureCategory
from src.common.domain.value_objects import TenantId, TenantPictureId


def build_tenant_picture(
    orm_instance: TenantPictureORM,
) -> TenantPicture:
    return TenantPicture(
        id=TenantPictureId(orm_instance.uuid),
        tenant_id=TenantId(orm_instance.tenant_id),
        category=TenantPictureCategory.from_value(orm_instance.category),
        label=orm_instance.label,
        image_url=orm_instance.image_url,
        created_at=orm_instance.created_at,
    )

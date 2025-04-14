from src.common.database.models import PendingActionORM
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.entities.pending_action import PendingAction
from src.common.domain.value_objects import PendingActionId


def build_pending_action(orm_instance: PendingActionORM) -> PendingAction:
    return PendingAction(
        id=PendingActionId(orm_instance.uuid),
        category=PendingActionCategory.from_value(orm_instance.category),
        status=PendingActionStatus.from_value(orm_instance.status),
        tracking_code=orm_instance.tracking_code,
        token=orm_instance.token,
        group_id=orm_instance.group_id,
        expired_at=orm_instance.expired_at,
        created_at=orm_instance.created_at,
        completed_at=orm_instance.completed_at,
        valid_until=orm_instance.valid_until,
        metadata=orm_instance.metadata,
        usage=orm_instance.usage,
        usage_limit=orm_instance.usage_limit,
    )

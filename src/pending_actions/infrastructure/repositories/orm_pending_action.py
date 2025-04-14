# -*- coding: utf-8 -*-
from typing import Optional

from django.db.models import Q

from src.common.database.models import PendingActionORM
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.pending_action import PendingAction
from src.common.infrastructure.builders.pending_action import build_pending_action
from src.pending_actions.domain.repositories import PendingActionRepository


class ORMPendingActionRepository(PendingActionRepository):
    def find(
        self,
        token_or_tracking_code: str,
        category: Optional[PendingActionCategory] = None,
        status: Optional[PendingActionStatus] = None,
    ) -> Optional[PendingAction]:
        filter_criteria = (
            Q(token=token_or_tracking_code) | Q(tracking_code=token_or_tracking_code)
        )

        if category:
            filter_criteria &= Q(category=str(category))
        if status:
            filter_criteria &= Q(status=str(status))

        try:
            return build_pending_action(
                orm_instance=PendingActionORM.objects.get(filter_criteria),
            )
        except PendingActionORM.DoesNotExist:
            return None


    def find_by_tracking_code(
        self,
        tracking_code: str,
    ) -> Optional[PendingAction]:
        try:
            return build_pending_action(
                orm_instance=PendingActionORM.objects.get(
                    tracking_code=tracking_code,
                ),
            )
        except PendingActionORM.DoesNotExist:
            return None

    def find_by_token(
        self,
        token: str,
        category: Optional[PendingActionCategory] = None,
        status: Optional[PendingActionStatus] = None,
    ) -> Optional[PendingAction]:
        filter_criteria = dict(token=token)

        if category:
            filter_criteria['category'] = str(category)
        if status:
            filter_criteria['status'] = str(status)

        try:
            return build_pending_action(
                orm_instance=PendingActionORM.objects.get(**filter_criteria),
            )
        except PendingActionORM.DoesNotExist:
            return None


    def persist(self, pending_action: PendingAction) -> PendingAction:
        orm_instance, _ = PendingActionORM.objects.update_or_create(
            uuid=pending_action.id,
            defaults=pending_action.to_persist_dict,
        )
        return build_pending_action(orm_instance)

    def persist_with_token(self, pending_action: PendingAction) -> PendingAction:
        orm_instance, _ = PendingActionORM.objects.update_or_create(
            token=pending_action.token,
            defaults=pending_action.to_persist_dict,
        )
        return build_pending_action(orm_instance)

    def expire_past_similars(
        self,
        group_id: str,
        category: PendingActionCategory,
    ):
        PendingActionORM.objects.filter(
            group_id=group_id,
            category=str(category),
            status=str(PendingActionStatus.PENDING),
        ).update(
            status=str(PendingActionStatus.EXPIRED),
        )

    def delete(self, pending_action: PendingAction):
        PendingActionORM.objects.filter(token=pending_action.token).delete()

    def cancel(self, pending_action: PendingAction):
        pending_action.cancel()
        self.persist(pending_action)

    def complete(self, pending_action: PendingAction):
        pending_action.complete()
        self.persist(pending_action)

    def delete_expired_actions(self):
        PendingActionORM.objects.filter(
            status=str(PendingActionStatus.EXPIRED)
        ).delete()

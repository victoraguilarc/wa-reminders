# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional

from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.pending_action import PendingAction


class PendingActionRepository(ABC):
    @abstractmethod
    def find(
        self,
        token_or_tracking_code: str,
        category: Optional[PendingActionCategory] = None,
        status: Optional[PendingActionStatus] = None,
    ) -> Optional[PendingAction]:
        raise NotImplementedError

    @abstractmethod
    def find_by_token(
        self,
        token: str,
        category: Optional[PendingActionCategory] = None,
        status: Optional[PendingActionStatus] = None,
    ) -> Optional[PendingAction]:
        raise NotImplementedError

    @abstractmethod
    def find_by_tracking_code(
        self,
        tracking_code: str,
    ) -> Optional[PendingAction]:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        pending_action: PendingAction,
    ) -> PendingAction:
        raise NotImplementedError

    @abstractmethod
    def persist_with_token(
        self,
        pending_action: PendingAction,
    ) -> PendingAction:
        raise NotImplementedError

    @abstractmethod
    def expire_past_similars(
        self,
        group_id: str,
        category: PendingActionCategory,
    ):
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        pending_action: PendingAction,
    ):
        raise NotImplementedError

    @abstractmethod
    def cancel(
        self,
        pending_action: PendingAction,
    ):
        raise NotImplementedError

    @abstractmethod
    def complete(
        self,
        pending_action: PendingAction,
    ):
        raise NotImplementedError

    @abstractmethod
    def delete_expired_actions(
        self,
    ):
        raise NotImplementedError

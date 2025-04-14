# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.models.pending_action import PendingAction


@dataclass
class PendingActionPresenter(object):
    instance: PendingAction

    @property
    def to_dict(self):
        return {
            **self.instance.to_tracking_dict,
            'metadata': self.instance.metadata,
            'expired_at': self.instance.expired_at,
            'completed_at': self.instance.completed_at,
            'valid_until': self.instance.valid_until,
        }

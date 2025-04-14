# -*- coding: utf-8 -*-

from src.common.domain.exceptions.common import BadRequest, NotFound


class InvalidPendingActionError(BadRequest):
    pass


class CorruptedPendingActionError(BadRequest):
    pass


class PendingActionNotFoundError(NotFound):
    pass

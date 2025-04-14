# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.context.locale import LocaleContext
from src.common.domain.enums.common import TaskResultStatus
from src.common.domain.interfaces.responses import ApiResponse
from src.common.helpers.time import TimeUtils


@dataclass
class TaskResultResponse(ApiResponse):
    status: TaskResultStatus = TaskResultStatus.SUCCESS

    def render(self, locale_context: LocaleContext) -> dict:
        local_now = TimeUtils.local_now(str(locale_context.time_zone))
        return {
            'status': str(self.status),
            'completed_at': local_now.isoformat(),
        }

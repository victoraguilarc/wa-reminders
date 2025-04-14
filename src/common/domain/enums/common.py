from src.common.domain import BaseEnum


class TaskResultStatus(BaseEnum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    IN_PROGRESS = 'IN_PROGRESS'
    FAILURE = 'FAILURE'

from src.common.domain import BaseEnum


class ReminderStatus(BaseEnum):
    PENDING = 'PENDING'
    ENQUEUED = 'ENQUEUED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class ReminderRecipientStatus(BaseEnum):
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'


    @property
    def is_sent(self) -> bool:
        return self == ReminderRecipientStatus.SENT

    @property
    def is_failed(self) -> bool:
        return self == ReminderRecipientStatus.FAILED

    @property
    def is_pending(self) -> bool:
        return self == ReminderRecipientStatus.PENDING

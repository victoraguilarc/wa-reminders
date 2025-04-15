from src.common.domain import BaseEnum


class ReminderStatus(BaseEnum):
    PENDING = 'PENDING'
    ENQUEUED = 'ENQUEUED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class ReminderRecipientStatus(BaseEnum):
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'

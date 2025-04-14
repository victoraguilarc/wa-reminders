# -*- coding: utf-8 -*-
from django.conf import settings

from src.common.domain.context.bus import BusContext
from src.common.helpers.singlenton import SingletonMeta
from src.common.infrastructure.messaging import MemoryCommandBus, MemoryEventBus, MemoryQueryBus
from src.common.infrastructure.messaging.sqs_task_scheduler import SQSTaskScheduler


class BusSingleton(metaclass=SingletonMeta):
    instance: BusContext = BusContext(
        command_bus=MemoryCommandBus(
            task_scheduler=SQSTaskScheduler(
                queue_url=settings.ASYNC_TASKS_QUEUE_URL,
            ),
        ),
        query_bus=MemoryQueryBus(),
        event_bus=MemoryEventBus(),
    )

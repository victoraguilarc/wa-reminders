# -*- coding: utf-8 -*-

# from django_grip import publish
from gripcontrol import HttpStreamFormat

from src.common.domain.entities.stream_event import StreamEvent
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher


class GripStreamEventPublisher(StreamEventPublisher):
    def publish(
        self,
        channel_id: str,
        stream_event: StreamEvent,
    ):
        pass
        # publish(
        #     channel_id,
        #     HttpStreamFormat(content=stream_event.to_raw),
        # )

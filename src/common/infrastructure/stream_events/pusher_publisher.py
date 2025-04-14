# -*- coding: utf-8 -*-
from dataclasses import dataclass

import pusher

from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.common.domain.models.stream_event import StreamEvent


@dataclass
class PusherStreamEventPublisher(StreamEventPublisher):
    pusher_client: pusher.Pusher

    def publish(
        self,
        channel_id: str,
        stream_event: StreamEvent,
    ):
        self.pusher_client.trigger(
            channels=channel_id,
            event_name=stream_event.event_name,
            data=stream_event.data,
        )

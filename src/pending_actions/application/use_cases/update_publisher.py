# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.stream_event import StreamEvent
from src.common.domain.events import PendingActionEvent
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher


@dataclass
class PendingActionSSEventPublisher(object):
    pending_action: PendingAction
    stream_events_publisher: StreamEventPublisher

    def execute(self):
        self.stream_events_publisher.publish(
            channel_id=self.pending_action.channel_id,
            stream_event=StreamEvent(
                event_name=str(PendingActionEvent.UPDATED),
                data=self.pending_action.to_tracking_dict,
            ),
        )

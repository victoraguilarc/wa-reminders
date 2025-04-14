# -*- coding: utf-8 -*-
from dataclasses import dataclass

from src.common.application.commands.notifications import PublishStreamEventCommand
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.common.domain.messaging.commands import CommandHandler


@dataclass
class PublishStreamEventHandler(CommandHandler):
    event_publisher: StreamEventPublisher

    def execute(
        self,
        command: PublishStreamEventCommand,
    ):
        self.event_publisher.publish(
            channel_id=command.channel_id,
            stream_event=command.stream_event,
        )

# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.common.domain.entities.stream_event import StreamEvent


@dataclass
class StreamEventPublisher(ABC):
    @abstractmethod
    def publish(
        self,
        channel_id: str,
        stream_event: StreamEvent,
    ):
        raise NotImplementedError

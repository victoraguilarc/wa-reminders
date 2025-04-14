# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from src.common.domain.messaging.events import DomainEvent


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent):
        raise NotImplemented('Not Implemented!')

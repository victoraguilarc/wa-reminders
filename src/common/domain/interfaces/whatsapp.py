from abc import ABC, abstractmethod


class WhatsappMessage(ABC):
    @property
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, kwargs: dict) -> 'WhatsappMessage':
        raise NotImplementedError

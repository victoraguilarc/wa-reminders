from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO


@dataclass
class QRCodeBuilder(ABC):
    @abstractmethod
    def build(self, value: str) -> BytesIO:
        raise NotImplementedError

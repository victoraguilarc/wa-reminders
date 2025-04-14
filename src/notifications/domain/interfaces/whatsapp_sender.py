from abc import ABC, abstractmethod

from src.common.domain.interfaces.whatsapp import WhatsappMessage


class WhatsappSender(ABC):
    @abstractmethod
    def send_message(
        self,
        session_name: str,
        phone_number: str,
        message: WhatsappMessage,
    ):
        raise NotImplementedError

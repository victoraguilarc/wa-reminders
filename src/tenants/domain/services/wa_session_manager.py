from abc import abstractmethod, ABC
from typing import List, Optional

from src.common.domain.models.wa_session import WhatsappSession, WhatsappSessionQRCode, WhatsappSessionWebhook


class WhatsappSessionManager(ABC):
    @abstractmethod
    def create_session(
        self,
        session_id: str,
        session_name: str,
        webhooks: List[WhatsappSessionWebhook] = None,
    ) -> WhatsappSession:
        raise NotImplementedError

    @abstractmethod
    def get_session(
        self,
        session_name: str,
    ) -> Optional[WhatsappSession]:
        raise NotImplementedError

    @abstractmethod
    def get_auth_qr(
        self,
        session_name: str,
    ) -> WhatsappSessionQRCode:
        raise NotImplementedError

    @abstractmethod
    def update_session(
        self,
        instance: WhatsappSession,
    ) -> WhatsappSession:
        raise NotImplementedError

    @abstractmethod
    def delete_session(
        self,
        session_name: str,
    ):
        raise NotImplementedError

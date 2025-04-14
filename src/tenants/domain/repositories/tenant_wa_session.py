# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional

from src.common.domain.models.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantWhatsappSessionId, TenantId


class TenantWhatsappSessionRepository(ABC):
    @abstractmethod
    def find(
        self,
        tenant_id: TenantId,
        instance_id: TenantWhatsappSessionId,
    ) -> Optional[TenantWhatsappSession]:
        raise NotImplementedError

    @abstractmethod
    def find_by_session_name(
        self,
        session_name: str,
    ) -> Optional[TenantWhatsappSession]:
        raise NotImplementedError

    @abstractmethod
    def get_messaging_session_name(
        self,
        tenant_id: TenantId,
    ) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def persist(
        self,
        tenant_id: TenantId,
        instance: TenantWhatsappSession,
    ) -> TenantWhatsappSession:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        tenant_id: TenantId,
        instance_id: TenantWhatsappSessionId,
    ):
        raise NotImplementedError

    @abstractmethod
    def filter(
        self,
        tenant_id: TenantId,
    ) -> List[TenantWhatsappSession]:
        raise NotImplementedError

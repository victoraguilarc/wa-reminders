# -*- coding: utf-8 -*-

import uuid
from dataclasses import dataclass
from typing import List

from src.common.application.helpers.strings import get_short_hash
from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.domain.interfaces.services import UseCase
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_wa_session import TenantWhatsappSession
from src.common.domain.models.wa_session import WhatsappSession, WhatsappSessionWebhook
from src.common.domain.value_objects import TenantWhatsappSessionId
from src.tenants.domain.exceptions import TenantWhatsappSessionsLimitReachedError
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionCreator(UseCase):
    tenant: Tenant
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager
    session_webhooks: List[WhatsappSessionWebhook]

    def execute(self) -> TenantWhatsappSession:
        if self._sessions_limit_reached():
            raise TenantWhatsappSessionsLimitReachedError

        device_id = uuid.uuid4()
        whatsapp_session = self.repository.persist(
            tenant_id=self.tenant.id,
            instance=self._build_instance(device_id),
        )
        remote_session = self._create_remote_session(whatsapp_session)

        # TODO: add other properties if its needed
        whatsapp_session.config = remote_session.config

        return self.repository.persist(self.tenant.id, whatsapp_session)

    def _build_instance(self, device_id: uuid.UUID) -> TenantWhatsappSession:
        return TenantWhatsappSession(
            id=TenantWhatsappSessionId(device_id),
            tenant=self.tenant,
            session_name=f'{self.tenant.slug}-{get_short_hash(str(device_id))}',
            status=WhatsappSessionStatus.STARTING,
        )

    def _sessions_limit_reached(self):
        sessions = self.repository.filter(tenant_id=self.tenant.id)
        return len(sessions) >= self.tenant.num_whatsapp_sessions

    def _create_remote_session(
        self,
        whatsapp_session: TenantWhatsappSession,
    ) -> WhatsappSession:
        return self.session_manager.create_session(
            session_id=str(whatsapp_session.id),
            session_name=whatsapp_session.session_name,
            webhooks=self.session_webhooks,
        )

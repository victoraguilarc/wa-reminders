from dataclasses import dataclass

from loguru import logger

from src.common.domain.enums.tenants import WhatsappSessionStatus
from src.common.domain.events import WhatsappSessionEvent
from src.common.domain.interfaces.services import UseCase
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.common.domain.entities.stream_event import StreamEvent
from src.tenants.application.whatsapp_sessions.mixins import GetTenantWhatsappSessionNameMixin
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class WhatsappSessionStatusUpdater(GetTenantWhatsappSessionNameMixin, UseCase):
    session_name: str
    status: WhatsappSessionStatus
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager
    stream_events_publisher: StreamEventPublisher

    def execute(self):
        local_session = self.get_by_session_name(
            session_name=self.session_name,
            raise_exception=False,
        )

        if not local_session:
            return

        remote_session = self.session_manager.get_session(self.session_name)

        logger.info(f'new_status: {self.status}')
        logger.info(f'remote_session: {remote_session.to_dict}')

        local_session.status = self.status
        self.repository.persist(tenant_id=local_session.tenant.id, instance=local_session)
        # Si el status es QR_CODE, Se debe consultar el codigo y enviarlo en el evento
        self.stream_events_publisher.publish(
            channel_id=local_session.session_name,
            stream_event=StreamEvent(
                event_name=str(WhatsappSessionEvent.STATUS_UPDATED),
                data={'status': str(self.status)},
            ),
        )

        trigger_refresh_sessions = (
            self.status in WhatsappSessionStatus.refresh_statuses()
            or (self.status.is_starting and not remote_session.is_linked)
        )

        if not trigger_refresh_sessions:
            return

        logger.info(f'\nREFRESH_SESSIONS: status={self.status}  me={remote_session.me}\n')
        self.stream_events_publisher.publish(
            channel_id=local_session.tenant.slug,
            stream_event=StreamEvent(
                event_name=str(WhatsappSessionEvent.REFRESH_SESSIONS),
                data={},
            ),
        )




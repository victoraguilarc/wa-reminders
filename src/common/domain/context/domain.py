# -*- coding: utf-8 -*-

from dataclasses import dataclass

from src.auth.domain.repositories import SessionRepository, SessionUserRepository
from src.common.domain.interfaces.stream_publisher import StreamEventPublisher
from src.notifications.domain.interfaces.email_sender import EmailSender
from src.notifications.domain.interfaces.whatsapp_sender import WhatsappSender
from src.notifications.domain.repositories.reminder import ReminderRepository
from src.pending_actions.domain.repositories import PendingActionRepository
from src.tenants.domain.repositories.tenant import TenantRepository
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager
from src.users.domain.repositories import TenantCustomerRepository
from src.users.domain.repositories.email_address import EmailAddressRepository
from src.users.domain.repositories.phone_number import PhoneNumberRepository
from src.users.domain.repositories.tenant_user import TenantUserRepository
from src.users.domain.repositories.user import UserRepository


@dataclass
class DomainContext(object):
    session_repository: SessionRepository

    # Common
    tenant_repository: TenantRepository
    whatsapp_session_manager: WhatsappSessionManager
    whatsapp_session_repository: TenantWhatsappSessionRepository

    # Users & Auth
    user_repository: UserRepository
    phone_number_repository: PhoneNumberRepository
    email_address_repository: EmailAddressRepository
    tenant_user_repository: TenantUserRepository
    tenant_customer_repository: TenantCustomerRepository
    session_user_repository: SessionUserRepository

    # Pending Actions
    pending_action_repository: PendingActionRepository

    # tenants
    stream_events_publisher: StreamEventPublisher

    # Notifications
    email_sender: EmailSender
    whatsapp_sender: WhatsappSender
    reminder_repository: ReminderRepository


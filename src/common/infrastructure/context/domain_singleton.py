# -*- coding: utf-8 -*-
import pusher
from django.conf import settings

from src.auth.infrastructure.repositories import (
    ORMSessionRepository,
    ORMSessionUserRepository,
)
from src.common.domain.context.domain import DomainContext
from src.common.helpers.singlenton import SingletonMeta
from src.common.infrastructure.stream_events.pusher_publisher import PusherStreamEventPublisher
from src.notifications.infrastructure.repositories.orm_reminder import ORMReminderRepository
from src.notifications.infrastructure.senders.django_email_sender import DjangoEmailSender
from src.notifications.infrastructure.senders.http_whatsapp_sender import HttpWhatsappSender
from src.pending_actions.infrastructure.repositories.orm_pending_action import ORMPendingActionRepository
from src.tenants.infrastructure.repositories.orm_tenant import ORMTenantRepository
from src.tenants.infrastructure.repositories.orm_tenant_wa_session import ORMTenantWhatsappSessionRepository
from src.tenants.infrastructure.services.http_wa_session_manager import HttpWhatsappSessionManager
from src.users.infrastructure.repositories import ORMTenantCustomerRepository
from src.users.infrastructure.repositories.orm_email_address import ORMEmailAddressRepository
from src.users.infrastructure.repositories.orm_phone_number import ORMPhoneNumberRepository
from src.users.infrastructure.repositories.orm_tenant_user import ORMTenantUserRepository
from src.users.infrastructure.repositories.orm_user import ORMUserRepository


class DomainSingleton(metaclass=SingletonMeta):
    instance: DomainContext = DomainContext(
        # Common
        session_repository=ORMSessionRepository(),
        whatsapp_session_manager=HttpWhatsappSessionManager(
            api_hostanme=settings.WHATSAPP_API_HOSTNAME,
            api_key=settings.WHATSAPP_API_KEY,
        ),
        # Users
        user_repository=ORMUserRepository(),
        phone_number_repository=ORMPhoneNumberRepository(),
        email_address_repository=ORMEmailAddressRepository(),
        tenant_repository=ORMTenantRepository(),
        tenant_user_repository=ORMTenantUserRepository(),
        tenant_customer_repository=ORMTenantCustomerRepository(),

        session_user_repository=ORMSessionUserRepository(),

        # Pending Actions
        pending_action_repository=ORMPendingActionRepository(),

        # Tenants
        whatsapp_session_repository=ORMTenantWhatsappSessionRepository(),

        stream_events_publisher=PusherStreamEventPublisher(
            pusher_client=pusher.Pusher(
                app_id=settings.PUSHER_APP_ID,
                key=settings.PUSHER_KEY,
                secret=settings.PUSHER_SECRET,
                host=settings.PUSHER_HOST,
                ssl=True,
            ),
        ),

        # Notifications
        email_sender=DjangoEmailSender(),
        whatsapp_sender=HttpWhatsappSender(
            api_hostanme=settings.WHATSAPP_API_HOSTNAME,
            api_key=settings.WHATSAPP_API_KEY,
        ),
        reminder_repository=ORMReminderRepository(),
    )

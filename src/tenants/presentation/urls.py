# -*- coding: utf-8 -*-

from django.urls import path

from src.tenants.presentation.api.tenant import TenantFromWhatsappSessionView
from src.tenants.presentation.api.tenant_wa_session import TenantWhatsappSessionView, TenantWhatsappSessionQRCodeView
from src.tenants.presentation.api.tenant_wa_session_webhook import TenantWhatsappSessionStatusWebhookView
from src.tenants.presentation.api.tenant_wa_sessions import TenantWhatsappSessionsView
from src.tenants.presentation.api.tenants import TenantsView

app_name = 'tenants'
urlpatterns = [
    path(
        'tenants/',
        view=TenantsView.as_view(),
        name='tenants',
    ),
    path(
        'tenants/from-whasapp-session/',
        view=TenantFromWhatsappSessionView.as_view(),
        name='tenant-from-wa-session',
    ),
    path(
        'whatsapp-sessions/',
        view=TenantWhatsappSessionsView.as_view(),
        name='whatsapp-sessions',
    ),
    path(
        'whatsapp-sessions/<uuid:whatsapp_session_id>/',
        view=TenantWhatsappSessionView.as_view(),
        name='whatsapp-session',
    ),
    path(
        'whatsapp-sessions/<uuid:whatsapp_session_id>/qr-code/',
        view=TenantWhatsappSessionQRCodeView.as_view(),
        name='whatsapp-session-qr-code',
    ),
    path(
        'whatsapp-sessions/<uuid:whatsapp_session_id>/auth-qr',
        view=TenantWhatsappSessionView.as_view(),
        name='whatsapp-session',
    ),
    # whatsapp-sessions webhooks
    path(
        'whatsapp-sessions/webhooks/status/',
        view=TenantWhatsappSessionStatusWebhookView.as_view(),
        name='whatsapp-session-status-webhook',
    ),
]

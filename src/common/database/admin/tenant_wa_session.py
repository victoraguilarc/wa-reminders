# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from src.common.database.models import TenantWhatsappSessionORM
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.common.infrastructure.context_builder import AppContextBuilder
from src.common.presentation.utils.admin_widgets import RelatedDropdownFilter
from src.tenants.application.whatsapp_sessions.use_cases.updater import TenantWhatsappSessionUpdater


@admin.action(description="Sync Remote Session")
def sync_remote_session(modeladmin, request, queryset):
    app_context = AppContextBuilder.from_env()
    wa_session_orm: TenantWhatsappSessionORM
    for wa_session_orm in queryset.all():
        TenantWhatsappSessionUpdater(
            tenant_id=TenantId(wa_session_orm.tenant_id),
            instance_id=TenantWhatsappSessionId(wa_session_orm.uuid),
            repository=app_context.domain.whatsapp_session_repository,
            session_manager=app_context.domain.whatsapp_session_manager,
        ).execute()



@admin.register(TenantWhatsappSessionORM)
class TenantWhatsappSessionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    actions = (sync_remote_session,)
    list_display = (
        'uuid',
        'tenant',
        'session_name',
        'status',
        'phone_number',
        'messaging_enabled',
    )
    raw_id_fields = ('tenant',)
    search_fields = ('phone_number', 'session_name')
    list_filter = (
        'status',
        ('tenant', RelatedDropdownFilter),
    )

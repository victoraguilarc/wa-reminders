# -*- coding: utf-8 -*-

from typing import List, Optional

from src.common.database.models.tenant_wa_session import TenantWhatsappSessionORM
from src.common.domain.models.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId, TenantWhatsappSessionId
from src.common.infrastructure.builders.tenant_wa_session import build_tenant_whatsapp_session
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository


class ORMTenantWhatsappSessionRepository(TenantWhatsappSessionRepository):
    def find(
        self,
        tenant_id: TenantId,
        instance_id: TenantWhatsappSessionId,
    ) -> Optional[TenantWhatsappSession]:
        try:
            orm_instance = (
                TenantWhatsappSessionORM.objects
                .select_related('tenant')
                .get(
                    tenant_id=tenant_id,
                    uuid=instance_id,
                )
            )
            return build_tenant_whatsapp_session(orm_instance)
        except TenantWhatsappSessionORM.DoesNotExist:
            return None

    def find_by_session_name(
        self,
        session_name: str,
    ) -> Optional[TenantWhatsappSession]:
        try:
            orm_instance = (
                TenantWhatsappSessionORM.objects
                .select_related('tenant')
                .get(session_name=session_name)
            )
            return build_tenant_whatsapp_session(orm_instance)
        except TenantWhatsappSessionORM.DoesNotExist:
            return None

    def get_messaging_session_name(
        self,
        tenant_id: TenantId,
    ) -> Optional[str]:
        orm_instance = TenantWhatsappSessionORM.objects.filter(
            tenant_id=tenant_id,
            agents_enabled=True
        ).order_by('-created_at').first()
        if orm_instance:
            return orm_instance.session_name
        return None

    def persist(
        self,
        tenant_id: TenantId,
        instance: TenantWhatsappSession,
    ) -> TenantWhatsappSession:
        orm_instance, _ = TenantWhatsappSessionORM.objects.update_or_create(
            tenant_id=tenant_id,
            uuid=instance.id,
            defaults=instance.to_persist_dict,
        )
        return build_tenant_whatsapp_session(orm_instance)

    def filter(self, tenant_id: TenantId) -> List[TenantWhatsappSession]:
        orm_instances = (
            TenantWhatsappSessionORM.objects
            .select_related('tenant')
            .filter(
                tenant_id=tenant_id,
            ).order_by('-created_at')
        )
        return [
            build_tenant_whatsapp_session(orm_instance)
            for orm_instance in orm_instances
        ]

    def delete(
        self,
        tenant_id: TenantId,
        instance_id: TenantWhatsappSessionId,
    ):
        instance_orm = TenantWhatsappSessionORM.objects.filter(
            uuid=instance_id,
            tenant_id=tenant_id,
        ).first()

        if instance_orm:
            instance_orm.delete()

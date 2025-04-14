# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from typing import List

from loguru import logger

from src.common.domain.interfaces.services import UseCase
from src.common.domain.models.tenant_wa_session import TenantWhatsappSession
from src.common.domain.value_objects import TenantId
from src.tenants.application.whatsapp_sessions.mixins import RefreshTenantWhatsappSessionMixin
from src.tenants.domain.repositories.tenant_wa_session import TenantWhatsappSessionRepository
from src.tenants.domain.services.wa_session_manager import WhatsappSessionManager


@dataclass
class TenantWhatsappSessionsLister(RefreshTenantWhatsappSessionMixin, UseCase):
    tenant_id: TenantId
    repository: TenantWhatsappSessionRepository
    session_manager: WhatsappSessionManager
    force_refresh: bool = False

    def execute(self) -> List[TenantWhatsappSession]:
        initial_instances = self.repository.filter(tenant_id=self.tenant_id)
        if self.force_refresh:
            return self.get_refreshed_instances(initial_instances)
        return initial_instances

    def get_refreshed_instances(
        self,
        instances: List[TenantWhatsappSession],
    ) -> List[TenantWhatsappSession]:
        if len(instances) == 0:
            return []
        return self._process_in_parallel(instances)

    def _process_in_parallel(
        self,
        instances: List[TenantWhatsappSession],
    ):
        refreshed_instances = []
        with ThreadPoolExecutor(len(instances)) as executor:
            futures = [
                executor.submit(self._refresh_single_instance, instance)
                for instance in instances
            ]
            wait(futures)

            for future in futures:
                result = future.result()
                if not result:
                    continue
                refreshed_instances.append(result)
                
        return refreshed_instances

    def _refresh_single_instance(
        self,
        instance: TenantWhatsappSession,
    ) -> TenantWhatsappSession:
        logger.info(f'Fetching session for: {instance.session_name}')
        return self.refresh_instance(instance)

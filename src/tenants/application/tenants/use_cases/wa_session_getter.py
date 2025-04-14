# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

from src.common.domain.interfaces.services import UseCase
from src.common.domain.models.tenant_wa_session import TenantWhatsappSession
from src.tenants.domain.exceptions import TenantNotFoundError
from src.tenants.domain.repositories.tenant import TenantRepository


@dataclass
class TenantFromWhatsappSessionGetter(UseCase):
    session_name: str
    repository: TenantRepository

    def execute(self) -> Optional[TenantWhatsappSession]:
        tenant_wa_session = self.repository.find_by_wa_session(
            session_name=self.session_name,
        )
        if not tenant_wa_session:
            raise TenantNotFoundError
        return tenant_wa_session


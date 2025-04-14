# -*- coding: utf-8 -*-

from unittest.mock import create_autospec

import pytest

from src.common.domain.messaging.commands import CommandBus
from src.tenants.domain.repositories.tenant import TenantRepository


@pytest.fixture
def tenant_repository():
    return create_autospec(spec=TenantRepository, spec_set=True, instance=True)


@pytest.fixture
def command_bus():
    return create_autospec(spec=CommandBus, spec_set=True, instance=True)

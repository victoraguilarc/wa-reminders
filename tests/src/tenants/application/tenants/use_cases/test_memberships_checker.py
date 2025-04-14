from unittest.mock import MagicMock, call

import pytest
from expects import be_false, be_true, equal, expect

from src.common.application.commands.memberships import RefreshMembershipsStatusCommand
from src.common.domain.models.tenant import Tenant
from src.common.domain.messaging.commands import CommandBus
from src.tenants.application.tenants.use_cases.memberships_checker import TenantMembershipsChecker
from src.tenants.domain.repositories.tenant import TenantRepository


@pytest.fixture(scope='function')
def use_case(
    tenant_repository: TenantRepository,
    command_bus: CommandBus,
):
    return TenantMembershipsChecker(
        repository=tenant_repository,
        command_bus=command_bus,
        run_async_refreshes=False,
    )


def test_execute_with_tenants(
    tenant_repository: MagicMock,
    command_bus: MagicMock,
    tenant: Tenant,
    use_case: TenantMembershipsChecker,
):
    tenant_repository.get_active_tenants.return_value = [tenant, tenant]

    use_case.execute()

    expect(tenant_repository.get_active_tenants.called).to(be_true)
    expect(command_bus.dispatch.call_args_list).to(
        equal(
            [
                call(
                    command=RefreshMembershipsStatusCommand(tenant_id=tenant.id),
                    run_async=False,
                ),
                call(
                    command=RefreshMembershipsStatusCommand(tenant_id=tenant.id),
                    run_async=False,
                ),
            ]
        )
    )


def test_execute_without_tenants(
    tenant_repository: MagicMock,
    command_bus: MagicMock,
    use_case: TenantMembershipsChecker,
):
    tenant_repository.get_active_tenants.return_value = []

    use_case.execute()

    expect(tenant_repository.get_active_tenants.called).to(be_true)
    expect(command_bus.dispatch.called).to(be_false)

from unittest.mock import Mock, call

import pytest
from expects import be_true, equal, expect
from pytest_mock import MockerFixture

from src.common.application.commands.tenants import CheckMembershipsStatusCommand
from src.common.domain.messaging.commands import CommandBus
from src.tenants.application.tenants.handlers.check_memberships import (
    CheckMembershipsStatusHandler,
)
from src.tenants.application.tenants.use_cases.memberships_checker import TenantMembershipsChecker
from src.tenants.domain.repositories.tenant import TenantRepository

base_path = 'src.tenants.application.tenants.handlers.check_memberships'


@pytest.fixture(scope='function')
def handler(
    tenant_repository: TenantRepository,
    command_bus: CommandBus,
):
    return CheckMembershipsStatusHandler(
        repository=tenant_repository,
        command_bus=command_bus,
    )


def test_execute(
    tenant_repository: TenantRepository,
    command_bus: CommandBus,
    handler: CheckMembershipsStatusHandler,
    mocker: MockerFixture,
):
    user_case_class_mock = mocker.patch(f'{base_path}.{TenantMembershipsChecker.__name__}')
    user_case_mock = Mock()
    user_case_class_mock.return_value = user_case_mock

    handler.execute(
        command=CheckMembershipsStatusCommand(
            run_async=False,
        ),
    )

    expect(user_case_class_mock.call_args).to(
        equal(
            call(
                repository=tenant_repository,
                run_async_refreshes=False,
                command_bus=command_bus,
            ),
        )
    )
    expect(user_case_mock.execute.called).to(be_true)

# -*- coding: utf-8 -*-

from src.common.application.commands.users import (
    CreateBasicTenantCustomerCommand,
    PersistEmailAddressCommand,
    PersistPhoneNumberCommand,
    RegisterCustomerInTenantCommand,
    RegisterUserCommand,
    RegisterUserInTenantCommand,
    PersistTenantCustomerCommand,
    PersistTenantUserCommand,
    SetUserPasswordCommand, DeactivateUserCommand,
)
from src.common.application.queries.users import (
    GetTenantCustomerByEmailQuery,
    GetTenantCustomerByIdQuery,
    GetTenantCustomerByParamsQuery,
    GetTenantCustomersByIdsQuery,
    GetUserByEmailQuery,
    GetTenantCustomerByAccessCodeQuery,
    GetOrCreatePhoneNumberQuery,
    GetOrCreateEmailAddressQuery,
    GetTenantUserByIdQuery,
    GetTenantUserByEmailQuery,
    GetTenantCustomerForSessionQuery,
    GetUserByIdQuery,
)
from src.common.infrastructure.context_builder import AppContextBuilder

from src.users.application.tenant_customers.handlers.create_tenant_customer import (
    CreateBasicTenantCustomerHandler,
    RegisterCustomerInTenantHandler,
)
from src.users.application.tenant_customers.handlers.create_tenant_user import (
    RegisterUserInTenantHandler,
)
from src.users.application.tenant_customers.handlers.get_tenant_customer import (
    GetTenantCustomerByEmailHandler,
    GetTenantCustomerByIdHandler,
    GetTenantCustomerByParamsHandler,
    GetTenantCustomerByAccessCodeHandler, GetTenantCustomerForSessionHandler,
)
from src.users.application.tenant_customers.handlers.get_tenant_customers import (
    GetTenantCustomersByIdsHandler,
)
from src.users.application.tenant_customers.handlers.persist_tenant_customer import (
    PersistTenantCustomerHandler,
)
from src.users.application.tenant_users.handlers.get_tenant_user import GetTenantUserByIdHandler, \
    GetTenantUserByEmailHandler
from src.users.application.tenant_users.handlers.persist_tenant_user import PersistTenantUserHandler
from src.users.application.users.handlers.deactivate_user import DeactivateUserHandler
from src.users.application.users.handlers.get_email_address import GetOrCreateEmailAddressHandler
from src.users.application.users.handlers.get_phone_number import GetOrCreatePhoneNumberHandler
from src.users.application.users.handlers.get_user import GetUserByEmailHandler, GetUserByIdHandler
from src.users.application.users.handlers.persist_assets import (
    PersistEmailAddressHandler,
    PersistPhoneNumberHandler,
)
from src.users.application.users.handlers.register_user import RegisterUserHandler
from src.users.application.users.handlers.set_user_password import SetUserPasswordHandler


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    # ~ C O M M A N D S

    bus.command_bus.subscribe(
        command=CreateBasicTenantCustomerCommand,
        handler=CreateBasicTenantCustomerHandler(
            repository=domain_context.tenant_customer_repository,
            command_bus=bus.command_bus,
        ),
    )
    bus.command_bus.subscribe(
        command=RegisterCustomerInTenantCommand,
        handler=RegisterCustomerInTenantHandler(
            repository=domain_context.tenant_customer_repository,
            command_bus=bus.command_bus,
        ),
    )
    bus.command_bus.subscribe(
        command=RegisterUserInTenantCommand,
        handler=RegisterUserInTenantHandler(
            repository=domain_context.tenant_user_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=RegisterUserCommand,
        handler=RegisterUserHandler(
            repository=domain_context.user_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=PersistPhoneNumberCommand,
        handler=PersistPhoneNumberHandler(
            repository=domain_context.phone_number_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=PersistEmailAddressCommand,
        handler=PersistEmailAddressHandler(
            repository=domain_context.email_address_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=PersistTenantCustomerCommand,
        handler=PersistTenantCustomerHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=PersistTenantUserCommand,
        handler=PersistTenantUserHandler(
            repository=domain_context.tenant_user_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=SetUserPasswordCommand,
        handler=SetUserPasswordHandler(
            repository=domain_context.user_repository,
        ),
    )
    bus.command_bus.subscribe(
        command=DeactivateUserCommand,
        handler=DeactivateUserHandler(
            repository=domain_context.user_repository,
        ),
    )

    #  Q U E R I E S

    bus.query_bus.subscribe(
        query=GetTenantCustomerByEmailQuery,
        handler=GetTenantCustomerByEmailHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetUserByEmailQuery,
        handler=GetUserByEmailHandler(
            repository=domain_context.user_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetUserByIdQuery,
        handler=GetUserByIdHandler(
            repository=domain_context.user_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomerByIdQuery,
        handler=GetTenantCustomerByIdHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantUserByIdQuery,
        handler=GetTenantUserByIdHandler(
            repository=domain_context.tenant_user_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantUserByEmailQuery,
        handler=GetTenantUserByEmailHandler(
            repository=domain_context.tenant_user_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomersByIdsQuery,
        handler=GetTenantCustomersByIdsHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomerByParamsQuery,
        handler=GetTenantCustomerByParamsHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomerForSessionQuery,
        handler=GetTenantCustomerForSessionHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomerByAccessCodeQuery,
        handler=GetTenantCustomerByAccessCodeHandler(
            repository=domain_context.tenant_customer_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetOrCreatePhoneNumberQuery,
        handler=GetOrCreatePhoneNumberHandler(
            repository=domain_context.phone_number_repository,
        ),
    )
    bus.query_bus.subscribe(
        query=GetOrCreateEmailAddressQuery,
        handler=GetOrCreateEmailAddressHandler(
            repository=domain_context.email_address_repository,
        ),
    )

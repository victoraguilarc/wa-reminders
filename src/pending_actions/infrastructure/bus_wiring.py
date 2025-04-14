from src.common.application.commands.pending_actions import (
    RequestTenantUserInvitationCommand, )
from src.common.application.queries.pending_actions import (
    GetEmailAddressVerificationQuery,
    GetPhoneNumberVerificationQuery,
    GetTenantCustomerSessionRedemptionQuery,
)
from src.common.infrastructure.context_builder import AppContextBuilder
from src.pending_actions.application.handlers.get_email_address_verification import (
    GetEmailAddressVerificationHandler,
)
from src.pending_actions.application.handlers.get_phone_number_verification import (
    GetPhoneNumberVerificationHandler,
)
from src.pending_actions.application.handlers.get_tenant_customer_session_redemption import (
    GetTenantCustomerSessionRedemptionHandler,
)
from src.pending_actions.application.handlers.request_tenant_user_invitation import (
    RequestTenantUserInvitationHandler,
)


def wire_handlers():
    app_context = AppContextBuilder.from_env()
    domain_context, bus = app_context.domain, app_context.bus

    #  Q U E R I E S

    bus.query_bus.subscribe(
        query=GetEmailAddressVerificationQuery,
        handler=GetEmailAddressVerificationHandler(
            action_repository=domain_context.pending_action_repository,
            query_bus=bus.query_bus,
            command_bus=bus.command_bus,
        ),
    )
    bus.query_bus.subscribe(
        query=GetPhoneNumberVerificationQuery,
        handler=GetPhoneNumberVerificationHandler(
            action_repository=domain_context.pending_action_repository,
            query_bus=bus.query_bus,
        ),
    )
    bus.query_bus.subscribe(
        query=GetTenantCustomerSessionRedemptionQuery,
        handler=GetTenantCustomerSessionRedemptionHandler(
            action_repository=domain_context.pending_action_repository,
        ),
    )

    #  C O M M A N D S
    bus.command_bus.subscribe(
        command=RequestTenantUserInvitationCommand,
        handler=RequestTenantUserInvitationHandler(
            query_bus=bus.query_bus,
            command_bus=bus.command_bus,
            pending_action_repository=domain_context.pending_action_repository,
        ),
    )




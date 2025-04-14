import json
from typing import Optional

from src.common.application.commands.notifications import (
    PublishStreamEventCommand,
    SendEmailCommand,
)
from src.common.domain.entities.membership import Membership
from src.common.domain.entities.stream_event import StreamEvent
from src.common.domain.entities.tenant import Tenant
from src.common.domain.entities.tenant_customer import TenantCustomer
from src.common.domain.events import TenantCustomerEvent
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.value_objects import TenantCustomerId


def send_membership_email_notification(
    command_bus: CommandBus,
    tenant: Tenant,
    tenant_customer: TenantCustomer,
    membership: Membership,
    template_name: str,
    action_link: Optional[str] = None,
):
    if not tenant_customer.email_address:
        return
    command_bus.dispatch(
        command=SendEmailCommand(
            to_emails=[tenant_customer.email_address.email],
            context={
                'tenant_name': tenant.name,
                'membership_plan_name': membership.membership_plan.name,
                'access_code': tenant_customer.access_code_url,
                'action_link': action_link,
            },
            template_name=template_name,
        ),
    )


def publish_membership_update(
    command_bus: CommandBus,
    tenant_customer_id: TenantCustomerId,
    run_async: bool = False,
):
    command_bus.dispatch(
        command=PublishStreamEventCommand(
            channel_id=TenantCustomer.build_channel_id(tenant_customer_id),
            stream_event=StreamEvent(
                event_name=str(TenantCustomerEvent.MEMBERSHIP_UPDATED),
                data={},
            ),
        ),
        run_async=run_async,
    )

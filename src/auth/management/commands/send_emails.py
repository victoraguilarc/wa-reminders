# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils.translation import activate

from src.common.application.commands.notifications import SendEmailCommand
from src.common.infrastructure.context_builder import AppContextBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_context = AppContextBuilder.from_env()
        domain_context, bus = app_context.domain, app_context.bus

        activate('es')

        user_email = 'vicobits@gmail.com'
        action_link = 'https://collectives.page'
        tenant_qa = 'QA'
        student = 'Victor Aguilar'
        membership_plan_name = '4 Clases'
        access_code_url = 'https://d3pzihcm2d2pr2.cloudfront.net/media/pictures/367bb708-c86f-4b21-8edc-4b43f0d2bf39.png'

        # MEMBERSHIP PURCHASE / PARTIALLY PAID
        bus.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[user_email],
                context={
                    'tenant_name': tenant_qa,
                    'membership_plan_name': membership_plan_name,
                    'access_code': access_code_url,
                    'action_link': action_link,
                },
                template_name='membership/purchase/partially_paid',
            ),
            run_async=False,
        )

        # MEMBERSHIP PURCHASE / PAID
        bus.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[user_email],
                context={
                    'tenant_name': tenant_qa,
                    'membership_plan_name': membership_plan_name,
                    'access_code': access_code_url,
                    'action_link': action_link,
                },
                template_name='membership/purchase/completed',
            ),
        )

        # MEMBERSHIP DEACTIVATION
        bus.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[user_email],
                context={'tenant_name': tenant_qa, 'action_link': action_link},
                template_name='membership/deactivation',
            ),
        )

        # MEMBERSHIP RENEWAL / PARTIALLY PAID
        bus.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[user_email],
                context={
                    'tenant_name': tenant_qa,
                    'membership_plan_name': membership_plan_name,
                    'access_code': access_code_url,
                    'action_link': action_link,
                },
                template_name='membership/recharge/partially_paid',
            ),
        )

        # MEMBERSHIP RENEWAL / PAID
        bus.command_bus.dispatch(
            command=SendEmailCommand(
                to_emails=[user_email],
                context={
                    'tenant_name': tenant_qa,
                    'membership_plan_name': membership_plan_name,
                    'access_code': access_code_url,
                    'action_link': action_link,
                },
                template_name='membership/recharge/completed',
            ),
        )

        # VERIFY EMAIL
        bus.command_bus.dispatch(
            SendEmailCommand(
                to_emails=[user_email],
                context={
                    'action_link': action_link,
                },
                template_name='actions/email_address/verification',
            )
        )

        # RESET PASSWORD
        bus.command_bus.dispatch(
            SendEmailCommand(
                to_emails=[user_email],
                context={
                    'action_link': action_link,
                },
                template_name='actions/phone_number/verification',
            )
        )

        # EMAIL LOGIN
        bus.command_bus.dispatch(
            SendEmailCommand(
                to_emails=[user_email],
                context={
                    'first_name': 'Victor',
                    'action_link': action_link,
                },
                template_name='actions/tenant_customer/session_redemption',
            ),
        )

        # NEW TENANT
        bus.command_bus.dispatch(
            SendEmailCommand(
                to_emails=[user_email],
                context={
                    'tenant_name': tenant_qa,
                },
                template_name='tenants/new_tenant',
            )
        )

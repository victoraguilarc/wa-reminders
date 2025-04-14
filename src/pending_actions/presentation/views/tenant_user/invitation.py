# -*- coding: utf-8 -*-
from typing import Optional

from django.shortcuts import render
from loguru import logger

from src.common.application.helpers.strings import clean_string
from src.common.application.queries.tenants import GetTenantByIdQuery
from src.common.application.queries.users import GetTenantUserByIdQuery
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.common.domain.models.simple_person import SimplePerson
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_user import TenantUser
from src.common.presentation.views.transaction_view import ActionView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.tenant_user.invitation_performer import TenantUserInvitationPerformer
from src.pending_actions.domain.exceptions import InvalidPendingActionError, CorruptedPendingActionError
from src.pending_actions.domain.types.tenant_user_invitation import TenantUserInvitation
from src.pending_actions.presentation.forms.invitation import TenantUserInvitationForm


class TenantUserInvitationView(ActionView):
    template_name = 'actions/tenant_user/invitation.html'
    success_template_name = 'actions/tenant_user/invitation_done.html'

    def get(self, request, token, **kwargs):
        pending_action = self._get_pending_action(token)

        if not pending_action:
            return render(request, self.invalid_template_name)

        metadata = TenantUserInvitation.from_dict(pending_action.metadata)
        tenant_user = self._get_tenant_user(metadata)
        if not tenant_user:
            return render(request, self.invalid_template_name)

        tenant = self._get_tenant(metadata)
        form = TenantUserInvitationForm(
            initial={
                'first_name': clean_string(tenant_user.first_name),
                'paternal_surname': clean_string(tenant_user.paternal_surname),
                'maternal_surname': clean_string(tenant_user.maternal_surname),
                'password': '',
            },
        )
        context = dict(
            form=form,
            email=tenant_user.email or metadata.email,
            tenant_name=tenant.name,
            pending_action=pending_action,
        )
        return render(request, self.template_name, context)

    def post(self, request, token, **kwargs):
        pending_action = self._get_pending_action(token)

        if not pending_action:
            return render(request, self.invalid_template_name)

        metadata = TenantUserInvitation.from_dict(pending_action.metadata)
        tenant_user = self._get_tenant_user(metadata)
        if not tenant_user:
            return render(request, self.invalid_template_name)

        tenant = self._get_tenant(metadata)
        form = TenantUserInvitationForm(data=request.POST)
        context = dict(
            form=form,
            email=tenant_user.email or metadata.email,
            tenant_name=tenant.name,
            pending_action=pending_action,
        )

        if pending_action and form.is_valid():
            action_result = self._perform_pending_action(pending_action, form.cleaned_data)

            if action_result.is_completed:
                return render(request, self.success_template_name, context)

        return render(request, self.template_name, context)

    def _get_tenant(
        self,
        metadata: TenantUserInvitation,
    ) -> Optional[Tenant]:
        return self.bus_context.query_bus.ask(
            query=GetTenantByIdQuery(
                tenant_id=metadata.tenant_id,
            ),
        )

    def _get_tenant_user(
        self,
        metadata: TenantUserInvitation,
    ) -> Optional[TenantUser]:
        return self.bus_context.query_bus.ask(
            query=GetTenantUserByIdQuery(
                tenant_id=metadata.tenant_id,
                tenant_user_id=metadata.tenant_user_id,
            ),
        )


    def _get_pending_action(self, token: str) -> Optional[PendingAction]:
        return PendingActionTokenGetter(
            token=token,
            category=PendingActionCategory.TENANT_USER_INVITATION,
            status=PendingActionStatus.PENDING,
            action_repository=self.domain_context.pending_action_repository,
            raise_exception=False,
        ).execute()

    def _perform_pending_action(
        self,
        pending_action: PendingAction,
        cleaned_data: dict,
    ) -> PendingActionResult:
        try:
            return TenantUserInvitationPerformer(
                pending_action=pending_action,
                action_repository=self.domain_context.pending_action_repository,
                command_bus=self.bus_context.command_bus,
                query_bus=self.bus_context.query_bus,
                user_person=SimplePerson(
                    first_name=cleaned_data.get('first_name'),
                    paternal_surname=cleaned_data.get('paternal_surname'),
                    maternal_surname=cleaned_data.get('maternal_surname'),
                ),
                password=cleaned_data.get('password'),
            ).execute()
        except (InvalidPendingActionError, CorruptedPendingActionError) as exc:
            logger.error(f'TenantUserInvitation error={exc}')
            return PendingActionResult.failure()



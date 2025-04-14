# -*- coding: utf-8 -*-

from typing import Optional

from django.contrib import messages
from django.shortcuts import render

from src.common.application.queries.users import GetUserByIdQuery
from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.common.domain.models.tenant_user import TenantUser
from src.common.presentation.views.transaction_view import ActionView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.user.reset_password_performer import (
    UserResetPasswordPerformer,
)
from src.pending_actions.domain.exceptions import CorruptedPendingActionError, InvalidPendingActionError
from src.pending_actions.domain.types.user_reset_password import UserResetPassword
from src.pending_actions.presentation.forms.reset_password import UserResetPasswordForm


class UserResetPasswordView(ActionView):
    template_name = 'actions/user/reset_password.html'
    success_template_name = 'actions/user/reset_password_done.html'
    inactive_template_name = 'actions/common/inactive_account.html'

    def get(self, request, token: str):
        pending_action = self._get_pending_action(token)

        if not pending_action:
            return render(request, self.invalid_template_name)

        context = dict(pending_action=pending_action)
        metadata = UserResetPassword.from_dict(pending_action.metadata)
        tenant_user = self._get_user(metadata)

        if tenant_user and not tenant_user.is_active:
            return render(request, self.inactive_template_name)

        return render(request, self.template_name, context)

    def post(self, request, token: str):
        pending_action = self._get_pending_action(token)

        if not pending_action:
            return render(request, self.invalid_template_name)

        form = UserResetPasswordForm(data=request.POST)
        context = dict(form=form, pending_action=pending_action)

        if pending_action and form.is_valid():
            new_password = form.cleaned_data['password1']
            action_result = self._perform_pending_action(request, pending_action, new_password)

            if action_result.is_completed:
                return render(request, self.success_template_name, context)

        return render(request, self.template_name, context)

    def _get_pending_action(self, token: str) -> Optional[PendingAction]:
        return PendingActionTokenGetter(
            token=token,
            category=PendingActionCategory.USER_RESET_PASSWORD,
            status=PendingActionStatus.PENDING,
            action_repository=self.domain_context.pending_action_repository,
            raise_exception=False,
        ).execute()

    def _perform_pending_action(
        self,
        request,
        pending_action: PendingAction,
        new_password: str,
    ) -> PendingActionResult:
        try:
            return UserResetPasswordPerformer(
                pending_action=pending_action,
                new_password=new_password,
                action_repository=self.domain_context.pending_action_repository,
                query_bus=self.bus_context.query_bus,
                command_bus=self.bus_context.command_bus,
            ).execute()
        except (InvalidPendingActionError, CorruptedPendingActionError) as exc:
            messages.warning(request, "Invalid Action")

            return PendingActionResult.failure()

    def _get_user(self, metadata: UserResetPassword) -> Optional[TenantUser]:
        return self.bus_context.query_bus.ask(
            query=GetUserByIdQuery(user_id=metadata.user_id),
        )

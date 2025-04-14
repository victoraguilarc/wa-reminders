# -*- coding: utf-8 -*-

from django.shortcuts import render

from src.common.domain.enums.users import PendingActionCategory, PendingActionStatus
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.pending_action_result import PendingActionResult
from src.common.presentation.views.transaction_view import ActionView
from src.pending_actions.application.use_cases.action_token_getter import PendingActionTokenGetter
from src.pending_actions.application.use_cases.email_address.verification_performer import (
    EmailAddressVerificationPerformer,
)
from src.pending_actions.domain.exceptions import InvalidPendingActionError, CorruptedPendingActionError
from src.pending_actions.domain.types.email_address_verification import EmailAddressVerification


class EmailAddressVerificationView(ActionView):
    template_name = 'actions/email_address/verification.html'

    def get(self, request, token, **kwargs):
        context = {}

        pending_action = PendingActionTokenGetter(
            token=token,
            category=PendingActionCategory.EMAIL_ADDRESS_VERIFICATION,
            status=PendingActionStatus.PENDING,
            action_repository=self.domain_context.pending_action_repository,
            raise_exception=False,
        ).execute()

        if not pending_action:
            return render(request, self.invalid_template_name)

        action_result = self._perform_pending_action(pending_action)

        if action_result.is_completed:
            action_metadata = EmailAddressVerification.from_dict(
                data=action_result.pending_action.metadata,
            )
            context['email'] = action_metadata.email
            context['is_completed'] = action_result.is_completed

        return render(request, self.template_name, context)


    def _perform_pending_action(self, pending_action: PendingAction) -> PendingActionResult:
        try:
            return EmailAddressVerificationPerformer(
                pending_action=pending_action,
                action_repository=self.domain_context.pending_action_repository,
                stream_events_publisher=self.domain_context.stream_events_publisher,
                command_bus=self.bus_context.command_bus,
                query_bus=self.bus_context.query_bus,
            ).execute()
        except (InvalidPendingActionError, CorruptedPendingActionError):
            return PendingActionResult.failure()

from src.common.application.commands.users import (
    PersistEmailAddressCommand,
    PersistPhoneNumberCommand,
)
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.pending_action import PendingAction
from src.common.domain.models.phone_number import PhoneNumber
from src.common.helpers.dicts import validate_mandatory
from src.pending_actions.domain.repositories import PendingActionRepository


class UpdatePendingActionMixin(object):
    """
    This increments the usage of a pending action and
    completes it if the usage limit is reached
    """
    action_repository: PendingActionRepository

    def _update_pending_action(
        self,
        pending_action: PendingAction,
    ) -> PendingAction:
        pending_action.increment_usage()
        if pending_action.is_usage_limit_reached:
            self.action_repository.complete(pending_action)
        return self.action_repository.persist(pending_action)


class PerformVerificationsMixin(object):
    """
    This verifies the email address and phone number of a user.
    if those values are included in the pending action metadata
    """
    command_bus: CommandBus

    def _perform_included_verifications(self, pending_action: PendingAction):

        if validate_mandatory(pending_action.metadata, 'unverified_email_address'):
            self._process_email_address(
                email_address=EmailAddress.from_dict(
                    data=pending_action.metadata['unverified_email_address'],
                )
            )

        if validate_mandatory(pending_action.metadata, 'unverified_phone_number'):
            self._process_phone_number(
                phone_number=PhoneNumber.from_dict(
                    verified_data=pending_action.metadata['unverified_phone_number'],
                ),
            )

    def _process_email_address(self, email_address: EmailAddress):
        email_address.is_verified = True
        self.command_bus.dispatch(command=PersistEmailAddressCommand(email_address))

    def _process_phone_number(self, phone_number: PhoneNumber):
        phone_number.is_verified = True
        self.command_bus.dispatch(command=PersistPhoneNumberCommand(phone_number))


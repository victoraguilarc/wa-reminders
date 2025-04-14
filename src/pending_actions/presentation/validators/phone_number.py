from src.common.presentation.validators.phone_number import PhoneNumberValidator
from src.pending_actions.presentation.validators.pending_action import PendingActionRequestValidator


class PhoneNumberVerificationRequestValidator(
    PendingActionRequestValidator,
    PhoneNumberValidator,
):
    """
    This class is responsible for validating the request data for the phone number verification
    """

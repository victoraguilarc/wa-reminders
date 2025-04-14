from dataclasses import dataclass

from src.common.application.commands.notifications import SendWhatsappSequenceCommand
from src.common.domain.enums.locales import Language
from src.common.domain.interfaces.services import UseCase
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.models.whatsapp_message import TemplateWhatsappMessage, TextWhatsappMessage
from src.common.domain.value_objects import RawPhoneNumber


@dataclass
class PhoneNumberVerificationNotifier(UseCase):
    raw_phone_number: RawPhoneNumber
    command_bus: CommandBus
    lang: Language
    callback_url: str

    def execute(self):
        self.command_bus.dispatch(
            command=SendWhatsappSequenceCommand(
                phone_number=self.raw_phone_number.international_number,
                messages=[
                    TemplateWhatsappMessage(
                        language=self.lang,
                        template_name='actions/phone_number/verification',
                    ),
                    TextWhatsappMessage(
                        content=self.callback_url,
                    )
                ],
            ),
        )

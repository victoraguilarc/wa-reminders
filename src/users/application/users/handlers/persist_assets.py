from dataclasses import dataclass

from src.common.application.commands.users import (
    PersistEmailAddressCommand,
    PersistPhoneNumberCommand,
)
from src.common.domain.messaging.commands import CommandHandler
from src.users.domain.repositories.email_address import EmailAddressRepository
from src.users.domain.repositories.phone_number import PhoneNumberRepository


@dataclass
class PersistPhoneNumberHandler(CommandHandler):
    repository: PhoneNumberRepository

    def execute(self, command: PersistPhoneNumberCommand):
        self.repository.persist(command.instance)


@dataclass
class PersistEmailAddressHandler(CommandHandler):
    repository: EmailAddressRepository

    def execute(self, command: PersistEmailAddressCommand):
        self.repository.persist(command.instance)

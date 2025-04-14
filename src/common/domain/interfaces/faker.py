from abc import ABC, abstractmethod


class FakerInterface(ABC):
    """It is a typing interface for the Faker class."""

    @abstractmethod
    def word(self) -> str:
        pass

    @abstractmethod
    def uuid4(self) -> str:
        pass

    @abstractmethod
    def sentence(self) -> str:
        pass

    @abstractmethod
    def ascii_free_email(self) -> str:
        pass

    @abstractmethod
    def paragraph(self) -> str:
        pass

    @abstractmethod
    def sha256(self) -> str:
        pass

    @abstractmethod
    def fake_username(self) -> str:
        pass

    @abstractmethod
    def email(self) -> str:
        pass

    @abstractmethod
    def first_name(self) -> str:
        pass

    @abstractmethod
    def last_name(self) -> str:
        pass

    @abstractmethod
    def simple_profile(self) -> dict:
        pass

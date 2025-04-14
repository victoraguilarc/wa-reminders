from abc import ABC
from typing import List, Optional


class EmailSender(ABC):
    def send_email(
        self,
        to_emails: List[str],
        context: dict,
        template_name: str,
        subject: Optional[str] = None,
        from_email: Optional[str] = None,
    ):
        raise NotImplementedError

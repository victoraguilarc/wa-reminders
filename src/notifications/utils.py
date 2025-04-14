import json
import re
from typing import List

from src.notifications.domain.notification_recipient import NotificationRecipient
from src.notifications.domain.notification_target import NotificationTarget

HTML_PATTERN = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def clean_html(raw_html: str) -> str:
    return re.sub(HTML_PATTERN, '', raw_html)


def serialize_contacts_info(instanced_contacts: List[NotificationRecipient]) -> str:
    return json.dumps([contact_info.to_dict for contact_info in instanced_contacts])


def deserialize_contacts_info(string_contacts: str) -> List[NotificationRecipient]:
    contacts_info_list = json.loads(string_contacts)
    return [
        NotificationRecipient.from_dict(contact_info_dict)
        for contact_info_dict in contacts_info_list
    ]


def serialize_recipients(instanced_recipients: List[NotificationTarget]) -> str:
    return json.dumps([recipient.to_dict for recipient in instanced_recipients])


def deserialize_recipients(string_recipients: str) -> List[NotificationTarget]:
    recipients_list = json.loads(string_recipients)
    return NotificationTarget.from_list(recipients_list)

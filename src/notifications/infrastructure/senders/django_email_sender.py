from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation

from src.common.constants import DEFAULT_LANGUAGE
from src.common.domain.enums.locales import Language
from src.notifications.domain.interfaces.email_sender import EmailSender


class DjangoEmailSender(EmailSender):
    def send_email(
        self,
        to_emails: List[str],
        context: dict,
        template_name: str,
        subject: Optional[str] = None,
        from_email: Optional[str] = None,
        language: Optional[Language] = DEFAULT_LANGUAGE,
    ):
        with translation.override(language.value):
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            message_text = f'emails/{template_name}/message.txt'
            message_html = f'emails/{template_name}/message.html'

            subject = subject or render_to_string(f'emails/{template_name}/subject.txt')
            subject = subject.replace('\n', '')
            text_body = render_to_string(template_name=message_text, context=context)
            html_body = render_to_string(template_name=message_html, context=context)

            email = EmailMultiAlternatives(
                subject=subject,
                from_email=from_email,
                to=to_emails,
                body=text_body,
            )
            if html_body:
                email.attach_alternative(html_body, 'text/html')
            email.send()

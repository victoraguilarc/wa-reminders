from dataclasses import dataclass
from typing import Optional

from src.common.constants import DEFAULT_LANGUAGE
from src.common.domain.enums.locales import Language
from src.common.domain.interfaces.whatsapp import WhatsappMessage


@dataclass
class TemplateWhatsappMessage(WhatsappMessage):
    template_name: str
    context: Optional[dict] = None
    language: Language = DEFAULT_LANGUAGE

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'TemplateWhatsappMessage':
        return cls(
            template_name=kwargs.get('template_name', ''),
            context=kwargs.get('context', {}),
            language=Language.from_value(
                value=kwargs.get('language', str(DEFAULT_LANGUAGE)),
            ),
        )

    @property
    def to_dict(self) -> dict:
        return {
            'template_name': self.template_name,
            'context': self.context or {},
            'language': str(self.language),
        }


@dataclass
class TextWhatsappMessage(WhatsappMessage):
    content: str

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'TextWhatsappMessage':
        return cls(content=kwargs['content'])

    @property
    def to_dict(self) -> dict:
        return {
            'content': self.content,
        }


@dataclass
class ImageWhatsappMessage(WhatsappMessage):
    image_url: str
    language: Language = DEFAULT_LANGUAGE
    caption_template: Optional[str] = None
    caption_context: Optional[dict] = None

    @classmethod
    def from_dict(cls, kwargs: dict) -> 'ImageWhatsappMessage':
        return cls(
            caption_template=kwargs.get('caption_template'),
            caption_context=kwargs.get('caption_context'),
            image_url=kwargs.get('image_url'),
        )

    @property
    def to_dict(self) -> dict:
        return {
            'caption_template': self.caption_template,
            'caption_context': self.caption_context,
            'image_url': self.image_url,
        }

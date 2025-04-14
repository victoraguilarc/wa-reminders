from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from typing import Optional

from src.common.domain.value_objects import PictureId


@dataclass
class Picture(object):
    id: PictureId
    image_url: Optional[str]
    created_at: Optional[datetime]

    @property
    def to_dict(self):
        return {
            'id': str(self.id),
            'image_url': self.image_url,
        }


@dataclass
class QRCode(Picture):
    content: str
    image: Optional[BytesIO] = None

    @property
    def to_dict(self):
        data = super().to_dict
        return {
            **data,
            'content': self.content,
        }

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypeVar
from uuid import UUID

from src.common.constants import DEFAULT_PAGINATION_PAGE_SIZE
from src.common.helpers.enconding import decode_base64, encode_base64

T = TypeVar('T')


@dataclass
class PageParams(object):
    index: Optional[str] = None
    size: Optional[int] = None

    def __post_init__(self):
        self.size = self.size or DEFAULT_PAGINATION_PAGE_SIZE

    @property
    def page_index(self) -> 'PageIndex':
        if self.index is None:
            return PageIndex.initial()
        try:
            return PageIndex.from_base64(self.index)
        except ValueError:
            return PageIndex.initial()

    @classmethod
    def from_query_params(cls, params: dict) -> 'PageParams':
        return cls(
            index=params.get('pageIndex', None),
            size=params.get('pageSize', None),
        )


@dataclass(frozen=True)
class PageIndex(object):
    value: Optional[datetime] = None
    uuid: Optional[UUID] = None

    @property
    def to_base64(self) -> Optional[str]:
        if not self.value or not self.uuid:
            return None
        return encode_base64(f'{self.value.isoformat()}|{self.uuid}')

    @classmethod
    def from_base64(cls, base64: str) -> 'PageIndex':
        decoded_value = decode_base64(base64)
        value, uuid = decoded_value.split('|')
        return cls(datetime.fromisoformat(value), UUID(uuid))

    @classmethod
    def initial(cls) -> 'PageIndex':
        return cls(value=None, uuid=None)


@dataclass
class Page(object):
    page_size: int
    next_index: PageIndex
    prev_index: PageIndex
    items: List[T] = None
    has_next: Optional[bool] = False
    has_prev: Optional[bool] = False

    def __post_init__(self):
        self.items = self.items or []

    @property
    def to_pagination_dict(self) -> dict:
        return {
            'page_size': self.page_size,
            'prev_index': self.prev_index.to_base64,
            'next_index': self.next_index.to_base64,
            'has_next': self.has_next,
            'has_prev': self.has_prev,
        }

    @classmethod
    def empty(
        cls,
        page_size: Optional[int] = DEFAULT_PAGINATION_PAGE_SIZE,
        items: List[T] = None,
    ) -> 'Page':
        return cls(
            page_size=page_size,
            next_index=PageIndex.initial(),
            prev_index=PageIndex.initial(),
            items=items or [],
            has_next=False,
            has_prev=False,
        )

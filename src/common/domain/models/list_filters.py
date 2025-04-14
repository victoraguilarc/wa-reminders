from dataclasses import dataclass
from typing import Optional

from src.common.constants import DEFAULT_PAGINATION_PAGE_SIZE
from src.common.domain.models.pagination import PageParams
from src.common.infrastructure.query_params import QueryParams


@dataclass
class ListFilters(object):
    search_term: Optional[str] = None
    page_size: Optional[int] = None
    page_index: Optional[int] = None

    @property
    def page_params(self) -> PageParams:
        return PageParams(index=self.page_index, size=self.page_size)

    @classmethod
    def from_params(cls, params: QueryParams) -> 'ListFilters':
        search_term = params.get_str(key='search', default=None)
        return ListFilters(
            search_term=search_term.strip() if search_term else None,
            page_size=params.get_int(key='page_size', default=DEFAULT_PAGINATION_PAGE_SIZE),
            page_index=params.get_int(key='page_index', default=None),
        )

    @property
    def is_initial_page(self) -> bool:
        return self.page_index == 1 or self.page_index is None

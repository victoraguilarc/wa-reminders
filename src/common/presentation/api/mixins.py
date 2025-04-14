from typing import List

from rest_framework.pagination import BasePagination
from rest_framework.request import Request

from src.common.domain.models.list_filters import ListFilters
from src.common.infrastructure.query_params import QueryParams


class PaginationMixin(object):
    paginator: BasePagination

    def paginated_response(self, request: Request, rendered_items: List):
        paginated_items = self.paginator.paginate_queryset(
            rendered_items,
            request,
        )
        return self.paginator.get_paginated_response(paginated_items)


class ListFiltersMixin(object):
    @classmethod
    def get_list_filters(cls, request) -> ListFilters:
        params = QueryParams(request.query_params)
        return ListFilters(
            search_term=params.get_str(key='search', default=None),
            page_size=params.get_int(key='page_size', default=None),
            page_index=params.get_str(key='page_index', default=None),
        )

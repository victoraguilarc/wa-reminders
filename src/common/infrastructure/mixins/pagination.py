from typing import Any, Callable, List, Tuple, Union

from django.core.paginator import EmptyPage
from django.db.models import QuerySet
from infinite_scroll_pagination import paginator

from src.common.constants import DEFAULT_PAGINATION_LOOKUP_FIELD
from src.common.domain.entities.pagination import Page, PageIndex, PageParams


class ORMPaginationMixin(object):
    @classmethod
    def _get_pagination_page(
        cls,
        page_params: PageParams,
        query_set: Union[QuerySet[Any], List[Any]],
        domain_builder: Callable,
        domain_builder_kwargs: dict = None,
        lookup_field: Union[str, Tuple[str, ...]] = DEFAULT_PAGINATION_LOOKUP_FIELD,
    ) -> 'Page':
        domain_builder_kwargs = domain_builder_kwargs or {}
        try:
            page = paginator.paginate(
                query_set=query_set,
                lookup_field=lookup_field,
                value=page_params.page_index.value,
                pk=page_params.page_index.uuid,
                per_page=page_params.size,
                move_to=paginator.NEXT_PAGE,
            )
            next_page: dict = page.next_page()
            prev_page: dict = page.prev_page()

            return Page(
                page_size=page_params.size,
                items=[
                    domain_builder(orm_instance, **domain_builder_kwargs)
                    for orm_instance in page
                ],
                has_next=page.has_next(),
                has_prev=page.has_previous(),
                prev_index=cls._get_page_index(prev_page),
                next_index=cls._get_page_index(next_page),
            )
        except EmptyPage:
            return Page.empty(page_params.size)

    @classmethod
    def _get_page_index(cls, next_page: dict) -> PageIndex:
        next_value = next_page.get('value')
        next_page_value = (
            next_value[0]
            if next_value and isinstance(next_value, tuple) and len(next_value) > 0
            else None
        )
        next_page_uuid = next_page.get('pk')
        return PageIndex(value=next_page_value, uuid=next_page_uuid)

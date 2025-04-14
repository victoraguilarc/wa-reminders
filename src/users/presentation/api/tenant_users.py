# -*- coding: utf-8 -*-
from django.conf import settings
from loguru import logger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.common.application.presenters.tenant_user import TenantUserPresenter
from src.common.application.responses.pagination import PaginationResponse
from src.common.domain.enums.users import TenantUserStatus
from src.common.domain.models.tenant_user import TenantUser
from src.common.domain.value_objects import TenantRoleId
from src.common.infrastructure.query_params import QueryParams
from src.common.presentation.api import RequiredTenantUserAPIView
from src.users.application.tenant_users.responses import TenantUserResponse
from src.users.application.tenant_users.use_cases.creator import TenantUserCreator
from src.users.application.tenant_users.use_cases.lister import TenantUsersLister
from src.users.domain.filters.tenant_users import TenantUsersFilters
from src.users.presentation.validators.tenant_user import CreateTenantUserValidator


class TenantUsersView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        current_page = TenantUsersLister(
            tenant_id=self.tenant_context.tenant.id,
            repository=self.domain_context.tenant_user_repository,
            list_filters=self._get_filters(request),
        ).execute()

        response = PaginationResponse(current_page, TenantUserPresenter)
        return Response(response.render(self.locale_context))

    def post(self, request, **kwargs):
        logger.info(f'request.data: {request.data}')
        validator = CreateTenantUserValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data
        tenant_user_data = validated_data.get('tenant_user', {})

        tenant_user = TenantUserCreator(
            repository=self.domain_context.tenant_user_repository,
            command_bus=self.bus_context.command_bus,
            query_bus=self.bus_context.query_bus,
            new_instance=TenantUser.from_payload(
                verified_data={
                    **tenant_user_data,
                    'tenant_id': self.tenant_context.tenant.id,
                },
            ),
            send_invitation=validated_data.get('send_invitation', False),
            send_async_invitation=not settings.DEBUG,
            tenant_role_id=(
                TenantRoleId(tenant_user_data.get('tenant_role_id'))
                if tenant_user_data.get('tenant_role_id') else None
            ),
        ).execute()

        response = TenantUserResponse(instance=tenant_user)
        return Response(
            response.render(self.locale_context),
            status=status.HTTP_201_CREATED,
        )

    @classmethod
    def _get_filters(cls, request: Request) -> TenantUsersFilters:
        params = QueryParams(request.query_params)
        return TenantUsersFilters(
            search_term=params.get_str(key='search', default=None),
            page_size=params.get_int(key='page_size', default=None),
            page_index=params.get_str(key='page_index', default=None),
            statuses=params.get_enum_list(
                key='statuses',
                enum_class=TenantUserStatus,
                default=None,
            ),
        )

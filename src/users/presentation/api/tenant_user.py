# -*- coding: utf-8 -*-
from loguru import logger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.entities.tenant_user import TenantUser
from src.common.domain.value_objects import TenantCustomerId, TenantUserId
from src.common.presentation.api import RequiredTenantUserAPIView
from src.users.application.tenant_users.responses import TenantUserResponse
from src.users.application.tenant_users.use_cases.deleter import TenantUserDeleter
from src.users.application.tenant_users.use_cases.detailer import TenantUserDetailer
from src.users.application.tenant_users.use_cases.updater import TenantUserUpdater
from src.users.presentation.validators.tenant_user import TenantUserValidator


class TenantUserView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_user = TenantUserDetailer(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=TenantCustomerId(kwargs.get('tenant_user_id')),
            repository=self.domain_context.tenant_user_repository,
        ).execute()

        response = TenantUserResponse(instance=tenant_user)
        return Response(response.render(self.locale_context))

    def put(self, request, **kwargs):
        logger.info(f'request: {request.data}')
        validator = TenantUserValidator(data=request.data)
        validator.is_valid(raise_exception=True)
        validated_data = validator.validated_data

        tenant_user = TenantUserUpdater(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=TenantCustomerId(kwargs.get('tenant_user_id')),
            repository=self.domain_context.tenant_user_repository,
            updated_instance=TenantUser.from_payload(validated_data),
            updated_fields=list(validated_data.keys()),
            query_bus=self.bus_context.query_bus,
        ).execute()

        response = TenantUserResponse(instance=tenant_user)
        return Response(response.render(self.locale_context))

    def delete(self, request, **kwargs):
        TenantUserDeleter(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=TenantUserId(kwargs.get('tenant_user_id')),
            repository=self.domain_context.tenant_user_repository,
        ).execute()

        return Response(
            TenantUserResponse().render(self.locale_context),
            status=status.HTTP_204_NO_CONTENT,
        )

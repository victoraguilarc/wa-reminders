# -*- coding: utf-8 -*-
from loguru import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.application.responses.generics import TaskResultResponse
from src.common.presentation.api.tenant_api import RequiredTenantUserAPIView
from src.users.application.tenant_users.use_cases.password_updater import TenantUserPasswordUpdater
from src.users.presentation.validators.tenant_user import TenantUserPasswordValidator


class TenantUserPasswordView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)


    def put(self, request, **kwargs):
        logger.info(f'request: {request.data}')
        
        validator = TenantUserPasswordValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        result_status = TenantUserPasswordUpdater(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=self.tenant_context.tenant_user.id,
            repository=self.domain_context.tenant_user_repository,
            current_password=validator.validated_data['current_password'],
            new_password=validator.validated_data['new_password'],
        ).execute()

        response = TaskResultResponse(status=result_status)
        return Response(response.render(self.locale_context))

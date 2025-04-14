# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.common.domain.models.tenant_user import TenantUser
from src.common.presentation.api.tenant_api import RequiredTenantUserAPIView
from src.users.application.tenant_users.responses import TenantUserResponse
from src.users.application.tenant_users.use_cases.deactivator import TenantUserProfileDeleter
from src.users.application.tenant_users.use_cases.detailer import TenantUserDetailer
from src.users.application.tenant_users.use_cases.updater import TenantUserUpdater
from src.users.presentation.validators.tenant_user import TenantUserValidator


class TenantUserProfileView(RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        tenant_user = TenantUserDetailer(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=self.tenant_context.tenant_user.id,
            repository=self.domain_context.tenant_user_repository,
        ).execute()

        response = TenantUserResponse(instance=tenant_user)
        return Response(response.render(self.locale_context))

    def put(self, request, **kwargs):
        validator = TenantUserValidator(data=request.data)
        validator.is_valid(raise_exception=True)

        tenant_user = TenantUserUpdater(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=self.tenant_context.tenant_user.id,
            repository=self.domain_context.tenant_user_repository,
            query_bus=self.bus_context.query_bus,
            updated_instance=TenantUser.from_payload(validator.validated_data),
            updated_fields=validator.validated_data.keys(),
        ).execute()

        response = TenantUserResponse(instance=tenant_user)
        return Response(response.render(self.locale_context))

    def delete(self, request, **kwargs):
        TenantUserProfileDeleter(
            tenant_id=self.tenant_context.tenant.id,
            tenant_user_id=self.tenant_context.tenant_user.id,
            repository=self.domain_context.tenant_user_repository,
            command_bus=self.bus_context.command_bus,
        ).execute()

        return Response(
            TenantUserResponse().render(self.locale_context),
            status=status.HTTP_200_OK,
        )



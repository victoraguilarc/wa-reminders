# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.common.presentation.api import PaginationMixin, RequiredTenantUserAPIView



class RemindersView(PaginationMixin, RequiredTenantUserAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        # # params = QueryParams(request.query_params)
        # # last_days = params.get_int('last_days', default=ONE_WEEK_DAYS)
        # #
        # # app_service = PastNotificationsGetter(
        # #     tenant_id=self.tenant_context.tenant.id,
        # #     notification_repository=self.domain_context.notification_repository,
        # #     filter_last_days=last_days,
        # # )
        #
        # response = app_service.execute()
        # return self.paginated_response(
        #     request,
        #     response.render(self.locale_context),
        # )
        return Response({"status": "ok"})

    def post(self, request, **kwargs):
        # validator = SendNotificationValidator(data=request.data)
        # validator.is_valid(raise_exception=True)
        # request_data = validator.validated_data
        #
        # app_service = NotificationRequester(
        #     tenant_id=self.tenant_context.tenant.id,
        #     subject=request_data['subject'],
        #     html_message=request_data['message'],
        #     targets=NotificationTarget.from_list(request_data['targets']),
        #     strategies=NotificationStrategy.from_list(request_data['strategies']),
        #     notification_repository=self.domain_context.notification_repository,
        #     command_bus=self.bus_context.command_bus,
        # )
        #
        # response = app_service.execute()
        # return Response(response.render(self.locale_context))
        return Response({"status": "ok"})

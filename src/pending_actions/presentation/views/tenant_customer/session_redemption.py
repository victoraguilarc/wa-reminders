# -*- coding: utf-8 -*-

from django.shortcuts import render

from src.common.presentation.views.transaction_view import ActionView


class TenantCustomerSessionRedemptionView(ActionView):
    def get(self, request, **kwargs):
        context = {}
        return render(
            request,
            'actions/common/inactive_feature.html',
            context,
        )

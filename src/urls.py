# -*- coding: utf-8 -*-

from django.urls import include, path

app_name = 'common'
urlpatterns = [
    path('v1/', include('src.auth.presentation.urls', namespace='auth')),
    path('v1/', include('src.tenants.presentation.urls', namespace='tenants')),
    path('v1/', include('src.users.presentation.urls', namespace='users')),
    path('v1/', include('src.notifications.presentation.urls', namespace='notifications')),
]

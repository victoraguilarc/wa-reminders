# -*- coding: utf-8 -*-

from django.urls import path

from src.notifications.presentation.api.notification import NotificationView
from src.notifications.presentation.api.notifications import NotificationsView

app_name = 'retention'
urlpatterns = [
    path(
        'notifications/',
        view=NotificationsView.as_view(),
        name='notifications',
    ),
    path(
        'notifications/<uuid:notification_id>/',
        view=NotificationView.as_view(),
        name='notification',
    ),
]

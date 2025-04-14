# -*- coding: utf-8 -*-

from django.urls import path

from src.reminders.presentation.api.app_release import AppReleaseView

app_name = 'resources'
urlpatterns = [
    path(
        'app-release/',
        view=AppReleaseView.as_view(),
        name='app-release',
    ),

]

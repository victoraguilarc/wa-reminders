# -*- coding: utf-8 -*-

from django.urls import include, path

app_name = 'common'
urlpatterns = [
    path('', include('src.pending_actions.presentation.views.urls', namespace='pending-actions')),
]

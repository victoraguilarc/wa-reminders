# -*- coding: utf-8 -*-

from django.urls import path

from src.auth.presentation.api.login import LoginView
from src.auth.presentation.api.register import RegisterView
from src.auth.presentation.api.session import SessionView

app_name = 'auth'
urlpatterns = [
    path(
        'auth/login/',
        view=LoginView.as_view(),
        name='login',
    ),
    path(
        'auth/session/',
        view=SessionView.as_view(),
        name='session',
    ),
    path(
        'auth/register/',
        view=RegisterView.as_view(),
        name='register',
    ),
]

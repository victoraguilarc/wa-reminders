# -*- coding: utf-8 -*-

from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView

app_name = 'common'
urlpatterns = [
    #
    # ~ EMAILS
    #
    path(
        'emails/verify-email/',
        TemplateView.as_view(
            template_name='emails/auth/../web/templates/actions/verify_email/message.html',
        ),
    ),
    path(
        'emails/reset-password/',
        TemplateView.as_view(
            template_name='emails/auth/../web/templates/actions/reset_password/message.html',
        ),
    ),
    path(
        'emails/new-tenant/',
        TemplateView.as_view(
            template_name='emails/auth/../web/templates/emails/tenants/new_tenant/message.html',
        ),
    ),
    path(
        'emails/student-enrollment/',
        TemplateView.as_view(
            template_name='emails/enrollments/../web/templates/emails/students/enrollments/complete/message.html',
        ),
    ),
    #
    # ~ PAGES & ERRORS
    #
    path('400/', TemplateView.as_view(template_name='errors/400.html'), name='error-400'),
    path('403/', TemplateView.as_view(template_name='errors/403.html'), name='error-403'),
    path('404/', TemplateView.as_view(template_name='errors/404.html'), name='error-404'),
    path('500/', TemplateView.as_view(template_name='errors/500.html'), name='error-500'),
    path('error/400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
    path(
        'error/403/',
        default_views.permission_denied,
        kwargs={'exception': Exception('Permission Denied')},
    ),
    path(
        'error/404/',
        default_views.page_not_found,
        kwargs={'exception': Exception('Page not Found')},
    ),
    path('error/500/', default_views.server_error),
]

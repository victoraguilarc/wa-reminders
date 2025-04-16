# -*- coding: utf-8 -*-
from django.urls import path

from src.notifications.presentation.api.reminder import ReminderView
from src.notifications.presentation.api.reminder_recipient import ReminderRecipientView
from src.notifications.presentation.api.reminder_recipients import ReminderRecipientsView
from src.notifications.presentation.api.reminders import RemindersView

app_name = 'notifications'
urlpatterns = [
    path(
        'reminders/',
        view=RemindersView.as_view(),
        name='reminders',
    ),
    path(
        'reminders/<uuid:reminder_id>/',
        view=ReminderView.as_view(),
        name='reminder',
    ),
    path(
        'reminders/<uuid:reminder_id>/recipients/',
        view=ReminderRecipientsView.as_view(),
        name='reminder-recipients',
    ),
    path(
        'reminders/<uuid:reminder_id>/recipients/<uuid:reminder_recipient_id>/',
        view=ReminderRecipientView.as_view(),
        name='reminder-recipient',
    ),
]

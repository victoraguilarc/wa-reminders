# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _

from src.common.presentation.api.exceptions.base import APIBadRequest

INVALID_PHONE_NUMBER = APIBadRequest(
    code='common.InvalidPhoneNumber',
    detail=_('Invalid Phone Number'),
)

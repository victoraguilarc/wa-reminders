# -*- coding: utf-8 -*-

from src.common.domain.exceptions.common import NotFound, UnAuthenticated


class InvalidCredentials(UnAuthenticated):
    pass


class InvalidCredentialsForTenant(UnAuthenticated):
    pass


class PictureNotFound(NotFound):
    pass


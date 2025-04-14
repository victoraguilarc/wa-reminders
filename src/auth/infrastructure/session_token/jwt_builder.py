# -*- coding: utf-8 -*-
from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken

from src.auth.domain.interfaces import UserSessionTokenBuilder
from src.common.domain.models.user import User
from src.common.domain.value_objects import UserSessionToken


class JWTUserSessionTokenBuilder(UserSessionTokenBuilder):
    def make_token(self, user: Union[User, AbstractBaseUser]) -> UserSessionToken:
        refresh = RefreshToken.for_user(user)
        return UserSessionToken(
            {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
        )

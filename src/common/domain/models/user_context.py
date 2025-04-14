from dataclasses import dataclass

from src.common.domain.models.user import User
from src.common.domain.models.user_profile import UserProfile


@dataclass
class UserContext(object):
    user: User
    profile: UserProfile

from dataclasses import dataclass

from src.common.domain.entities.user import User
from src.common.domain.entities.user_profile import UserProfile


@dataclass
class UserContext(object):
    user: User
    profile: UserProfile

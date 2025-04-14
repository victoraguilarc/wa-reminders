from dataclasses import dataclass

from src.common.domain.value_objects import UserId


@dataclass
class UserResetPassword(object):
    user_id: UserId
    email: str

    @property
    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'email': self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=UserId(data.get('user_id')),
            email=data.get('email'),
        )

    @property
    def is_valid(self):
        return bool(self.user_id and self.email)

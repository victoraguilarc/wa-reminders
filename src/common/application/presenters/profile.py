from dataclasses import dataclass

from src.common.domain.models.user_profile import UserProfile


@dataclass
class UserProfilePresenter(object):
    instance: UserProfile

    @property
    def to_dict(self):
        return {
            'id': str(self.instance.id),
            'user_id': str(self.instance.user_id),
            'first_name': self.instance.first_name,
            'paternal_surname': self.instance.paternal_surname,
            'maternal_surname': self.instance.maternal_surname,
            'email_address': (
                self.instance.email_address.to_minimal_dict if self.instance.email_address else None
            ),
            'phone_number': (
                self.instance.phone_number.to_minimal_dict if self.instance.phone_number else None
            ),
            'lang': str(self.instance.lang),
            'photo_url': self.instance.photo_url,
            'qr_passcode_url': self.instance.qr_passcode_url,
            'display_name': self.instance.display_name,
            'display_email': self.instance.display_email,
            'display_phone': self.instance.display_phone,
        }

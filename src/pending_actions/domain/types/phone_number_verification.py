from dataclasses import dataclass

from src.common.domain.value_objects import PhoneNumberId, RawPhoneNumber


@dataclass
class PhoneNumberVerification(object):
    phone_number_id: PhoneNumberId
    raw_phone_number: RawPhoneNumber

    @property
    def to_dict(self):
        return {
            'phone_number_id': str(self.phone_number_id),
            'raw_phone_number': self.raw_phone_number.to_dict,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            phone_number_id=PhoneNumberId(data.get('phone_number_id')),
            raw_phone_number=RawPhoneNumber.from_dict(
                instance_data=data.get('raw_phone_number'),
            ),
        )

    @property
    def is_valid(self):
        return bool(self.phone_number_id and self.raw_phone_number)

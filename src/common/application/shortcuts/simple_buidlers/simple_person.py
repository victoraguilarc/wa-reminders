from typing import Optional

from src.common.application.shortcuts.simple_buidlers.raw_phone_number import RawPhoneNumberBuilder
from src.common.domain.entities.simple_person import SimplePerson
from src.common.domain.value_objects import RawPhoneNumber


class SimplePersonBuilder(object):
    @classmethod
    def build_from_data(cls, validated_data: dict) -> SimplePerson:
        return SimplePerson(
            first_name=validated_data.get('first_name'),
            paternal_surname=validated_data.get('paternal_surname'),
            maternal_surname=validated_data.get('maternal_surname'),
            email=validated_data.get('email'),
            phone_number=cls.build_phone_number(validated_data.get('phone_number') or {}),
        )

    @classmethod
    def build_phone_number(cls, validated_data: dict) -> Optional[RawPhoneNumber]:
        data_keys = list(validated_data.keys())
        if not ('dial_code' in data_keys and 'phone_number' in data_keys):
            return None
        return RawPhoneNumberBuilder.build(
            dial_code=validated_data.get('dial_code'),
            phone_number=validated_data.get('phone_number'),
        )

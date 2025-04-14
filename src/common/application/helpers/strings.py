import hashlib
from typing import Optional


def clean_string(raw_input: Optional[str]):
    if raw_input is None:
        return ''
    return raw_input


def get_short_hash(input_string: str, length=7):
    full_hash = hashlib.sha1(input_string.encode()).hexdigest()
    return full_hash[:length]

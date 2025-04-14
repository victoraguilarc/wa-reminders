from typing import Any

import shortuuid


def alias_generator():
    return shortuuid.uuid()


def is_empty_data(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value == '')

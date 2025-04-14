from typing import Optional, Any


def optional_str(value: Optional[Any]) -> Optional[str]:
    return str(value) if value else None

from dataclasses import dataclass, asdict

from dacite import from_dict


@dataclass
class TenantMessage(object):
    label: str
    content: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantMessage':
        return from_dict(data_class=TenantMessage, data=data)

from dataclasses import dataclass, asdict

from dacite import from_dict


@dataclass
class TenantLocation(object):
    lat: str
    lng: str
    address: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantLocation':
        return from_dict(data_class=TenantLocation, data=data)

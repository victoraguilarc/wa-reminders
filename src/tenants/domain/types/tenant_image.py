from dataclasses import dataclass, asdict

from dacite import from_dict


@dataclass
class TenantImage(object):
    label: str
    image_url: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantImage':
        return from_dict(data_class=TenantImage, data=data)

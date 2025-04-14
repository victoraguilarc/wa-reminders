from dataclasses import dataclass, asdict

from dacite import from_dict


@dataclass
class TenantLink(object):
    text: str
    url: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantLink':
        return from_dict(data_class=TenantLink, data=data)


@dataclass
class TenantSocialMedia(TenantLink):
    icon: str
    label: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantSocialMedia':
        return from_dict(data_class=TenantSocialMedia, data=data)

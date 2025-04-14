from dataclasses import dataclass, asdict

from dacite import from_dict


@dataclass
class TenantTestimonial(object):
    customer_photo_url: str
    customer_name: str
    message: str

    @property
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'TenantTestimonial':
        return from_dict(data_class=TenantTestimonial, data=data)

from dataclasses import dataclass
from typing import List, Union

from src.tenants.domain.types.tenant_image import TenantImage
from src.tenants.domain.types.tenant_link import TenantLink, TenantSocialMedia
from src.tenants.domain.types.tenant_location import TenantLocation
from src.tenants.domain.types.tenant_message import TenantMessage
from src.tenants.domain.types.tenant_testimonial import TenantTestimonial

TenantResourceContent = Union[
    TenantImage,
    TenantLink,
    TenantTestimonial,
    TenantLocation,
    TenantSocialMedia,
    TenantMessage,
]

@dataclass
class TenantResources(object):
    images: List[TenantImage]
    links: List[TenantLink]
    testimonials: List[TenantTestimonial]
    locations: List[TenantLocation]
    social_media: List[TenantSocialMedia]
    messages: List[TenantMessage]

    @property
    def to_dict(self):
        return {
            'images': [image.to_dict for image in self.images],
            'links': [link.to_dict for link in self.links],
            'testimonials': [testimonial.to_dict for testimonial in self.testimonials],
            'locations': [location.to_dict for location in self.locations],
            'social_media': [social_media.to_dict for social_media in self.social_media],
            'messages': [message.to_dict for message in self.messages],
        }

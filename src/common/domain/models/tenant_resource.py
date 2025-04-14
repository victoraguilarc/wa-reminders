from dataclasses import dataclass
from typing import Union

from src.common.domain.enums.tenants import TenantResourceCategory
from src.common.domain.value_objects import TenantResourceId


@dataclass
class TenantResource(object):
    id: TenantResourceId
    category: TenantResourceCategory
    content: Union[dict, list]

    @property
    def is_video(self) -> bool:
        return self.category == TenantResourceCategory.VIDEO

    @property
    def is_image(self) -> bool:
        return self.category == TenantResourceCategory.IMAGE

    @property
    def is_link(self) -> bool:
        return self.category == TenantResourceCategory.LINK

    @property
    def is_location(self) -> bool:
        return self.category == TenantResourceCategory.LOCATION

    @property
    def is_testimonial(self) -> bool:
        return self.category == TenantResourceCategory.TESTIMONIAL

    @property
    def is_social_media(self) -> bool:
        return self.category == TenantResourceCategory.SOCIAL_MEDIA

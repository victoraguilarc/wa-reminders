from dataclasses import dataclass
from typing import Dict

from src.common.domain.context.locale import LocaleContext
from src.common.domain.types.permission import Permission


@dataclass
class PermissionPresenter(object):
    instance: Permission
    locale_context: LocaleContext

    @property
    def to_dict(self) -> Dict:
        return {
            'key': self.instance.key,
            'label': self.instance.label,
        }

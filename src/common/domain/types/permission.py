import re
from dataclasses import dataclass
from typing import Optional

from src.common.domain import BaseEnum
from src.common.domain.exceptions.permissions import InvalidPermissionError


class PermissionNamespace(BaseEnum):
    CUSTOMERS = 'customers'
    COLLABORATORS = 'collaborators'
    LEADS = 'leads'
    MEMBERSHIPS = 'memberships'
    PLANS = 'plans'
    PAYMENTS = 'payments'
    CLASSES = 'classes'
    SESSIONS = 'sessions'
    ATTENDEES = 'attendees'
    METRICS = 'metrics'
    EVENTS = 'events'
    ROLES = 'roles'
    QUICK_ACTIONS = 'quickActions'
    UNKNOWN = 'unknown'


class PermissionAction(BaseEnum):
    VIEW = 'view'
    LIST = 'list'
    CREATE = 'create'
    EDIT = 'edit'
    DELETE = 'delete'
    OPEN_SCAN = 'openScanner'
    REGISTER_MEMBERSHIP = 'registerMembership'
    UNKNOWN = 'unknown'


@dataclass
class Permission(object):
    namespace: PermissionNamespace
    action: PermissionAction
    label: Optional[str] = None

    def __eq__(self, other) -> bool:
        return self.key == other.key

    @property
    def key(self) -> str:
        return f'{self.namespace.value}.{self.action.value}'

    @property
    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'label': self.label,
        }

    @classmethod
    def is_valid(cls, key_perm: str) -> bool:
        return bool(re.match(r'^[a-z_A-Z]+\.[a-z_A-Z]+$', key_perm))

    @classmethod
    def validate(cls, raw_perm: str) -> None:
        if not cls.is_valid(raw_perm):
            raise InvalidPermissionError

    @classmethod
    def from_key(cls, key_perm: str) -> 'Permission':
        cls.validate(key_perm)
        namespace, action = key_perm.split('.')
        return cls(
            namespace=PermissionNamespace.from_value(namespace) or PermissionNamespace.UNKNOWN,
            action=PermissionAction.from_value(action) or PermissionAction.UNKNOWN,
        )

    @classmethod
    def from_dict(cls, data: dict) -> 'Permission':
        return cls.from_key(key_perm=data.get('key', 'common.unknown'))

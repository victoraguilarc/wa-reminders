from dataclasses import dataclass

from src.common.domain.value_objects import TenantId, TenantUserId


@dataclass
class TenantUserInvitation(object):
    tenant_id: TenantId
    tenant_user_id: TenantUserId
    email: str

    @property
    def to_dict(self):
        return {
            'tenant_user_id': str(self.tenant_user_id),
            'tenant_id': str(self.tenant_id),
            'email': self.email,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            tenant_user_id=TenantUserId(data.get('tenant_user_id')),
            tenant_id=TenantId(data.get('tenant_id')),
            email=data.get('email'),
        )

    @property
    def is_valid(self):
        return bool(self.tenant_user_id and self.tenant_id)

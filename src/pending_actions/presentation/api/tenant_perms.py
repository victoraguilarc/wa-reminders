from src.common.domain.exceptions.users import NotEnoughTenantPermissions


class TenantUserPermissionsMixin(object):
    tenant_context = None

    def validate_tenant_permissions(self):
        is_authorized = self.tenant_context.tenant_user is not None
        if not is_authorized:
            raise NotEnoughTenantPermissions

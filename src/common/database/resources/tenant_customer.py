from import_export import resources

from src.common.database.models import TenantCustomerORM


class TenantCustomerAdminResource(resources.ModelResource):
    class Meta:
        model = TenantCustomerORM

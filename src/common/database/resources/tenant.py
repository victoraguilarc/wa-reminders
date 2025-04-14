from import_export import resources

from src.common.database.models import TenantORM


class TenantAdminResource(resources.ModelResource):
    class Meta:
        model = TenantORM

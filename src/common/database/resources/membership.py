from import_export import resources

from src.common.database.models import MembershipORM


class MembershipAdminResource(resources.ModelResource):
    class Meta:
        model = MembershipORM

from src.common.database.models import MembershipTenantCustomerORM
from src.tenants.domain.types.dashboard.tenant_activation import TenantActivation


def build_tenant_activation(
    orm_instance: MembershipTenantCustomerORM,
) -> TenantActivation:
    return TenantActivation(
        full_name=orm_instance.tenant_customer.display_name,
        email=orm_instance.tenant_customer.email,
        phone_number=orm_instance.tenant_customer.phone,
        amount=orm_instance.membership.membership_plan.amount,
        activation_date=orm_instance.created_at,
    )

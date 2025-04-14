from src.common.domain.entities.tenant import Tenant


def build_tenant_subdomain(
    hostname: str,
    tenant: Tenant,
    https: bool = True,
):
    protocol = 'https' if https else 'http'
    return f'{protocol}://{tenant.slug}.{hostname}/'


def build_domain(
    hostname: str,
    https: bool = True,
):
    protocol = 'https' if https else 'http'
    return f'{protocol}://{hostname}/'


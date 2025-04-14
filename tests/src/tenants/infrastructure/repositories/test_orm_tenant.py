import pytest
from expects import be_a, be_empty, equal, expect

from src.common.database.models.factories.tenant import TenantORMFactory
from src.common.domain.enums.tenants import TenantStatus
from src.tenants.infrastructure.repositories.orm_tenant import ORMTenantRepository


@pytest.fixture(scope='function')
@pytest.mark.django_db
def repository():
    return ORMTenantRepository()


@pytest.mark.django_db
def test_get_active_tenants(
    repository: ORMTenantRepository,
):
    active_tenants = 2
    TenantORMFactory.create_batch(active_tenants, status=str(TenantStatus.ACTIVE))
    TenantORMFactory.create_batch(1, status=str(TenantStatus.INACTIVE))

    result = repository.get_active_tenants()

    expect(result).to(be_a(list))
    expect(len(result)).to(equal(active_tenants))


@pytest.mark.django_db
def test_get_active_tenants_empty(
    repository: ORMTenantRepository,
):
    result = repository.get_active_tenants()

    expect(result).to(be_a(list))
    expect(result).to(be_empty)

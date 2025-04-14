import uuid

import pytest
from expects import be_a, equal, expect, have_keys

from src.common.application.commands.payments import (
    SyncCustomerTenantCustomerCommand,
    SyncPriceMembershipPlanCommand,
    SyncProductTenantClassCommand,
)
from src.common.domain.enums.payments import PaymentProvider
from src.common.domain.value_objects import (
    MembershipPlanId,
    TenantClassId,
    TenantCustomerId,
    TenantId,
)

# -> SyncProductTenantClassCommand
pytest.skip(allow_module_level=True)


@pytest.fixture(scope='function')
def sync_product_tenant_class() -> SyncProductTenantClassCommand:
    return SyncProductTenantClassCommand(
        tenant_id=TenantId(uuid.uuid4()),
        tenant_class_id=TenantClassId(uuid.uuid4()),
        payment_provider=PaymentProvider.STRIPE,
        sync_tenant_class=True,
        sync_payment_plans=False,
    )


def test_sync_product_tenant_class_to_dict(
    sync_product_tenant_class: SyncProductTenantClassCommand,
):
    command_dict = sync_product_tenant_class.to_dict

    expect(command_dict).to(be_a(dict))
    expect(command_dict).to(
        have_keys(
            {
                'tenant_id': str(sync_product_tenant_class.tenant_id),
                'tenant_class_id': str(sync_product_tenant_class.tenant_class_id),
                'payment_provider': str(sync_product_tenant_class.payment_provider),
                'sync_tenant_class': True,
                'sync_payment_plans': False,
            }
        )
    )


def test_sync_product_tenant_class_from_dict(
    sync_product_tenant_class: SyncProductTenantClassCommand,
):
    command_instance = SyncProductTenantClassCommand.from_dict(sync_product_tenant_class.to_dict)

    expect(command_instance).to(be_a(SyncProductTenantClassCommand))
    expect(command_instance).to(equal(sync_product_tenant_class))


# -> SyncPricePaymentPlanCommand


@pytest.fixture(scope='function')
def sync_price_membership_plan() -> SyncPriceMembershipPlanCommand:
    return SyncPriceMembershipPlanCommand(
        tenant_id=TenantId(uuid.uuid4()),
        membership_plan_id=MembershipPlanId(uuid.uuid4()),
        payment_provider=PaymentProvider.STRIPE,
    )


def test_sync_price_payment_plan_to_dict(sync_price_payment_plan: SyncPriceMembershipPlanCommand):
    command_dict = sync_price_payment_plan.to_dict

    expect(command_dict).to(be_a(dict))
    expect(command_dict).to(
        have_keys(
            {
                'tenant_id': str(sync_price_payment_plan.tenant_id),
                'payment_plan_id': str(sync_price_payment_plan.membership_plan_id),
                'payment_provider': str(sync_price_payment_plan.payment_provider),
            }
        )
    )


def test_sync_price_payment_plan_from_dict(sync_price_payment_plan: SyncPriceMembershipPlanCommand):
    command_instance = SyncPriceMembershipPlanCommand.from_dict(sync_price_payment_plan.to_dict)

    expect(command_instance).to(be_a(SyncPriceMembershipPlanCommand))
    expect(command_instance).to(equal(sync_price_payment_plan))


# -> SyncCustomerTenantCustomerCommand


@pytest.fixture(scope='function')
def sync_customer_tenant_customer() -> SyncCustomerTenantCustomerCommand:
    return SyncCustomerTenantCustomerCommand(
        tenant_id=TenantId(uuid.uuid4()),
        tenant_customer_id=TenantCustomerId(uuid.uuid4()),
        payment_provider=PaymentProvider.STRIPE,
    )


def test_sync_customer_tenant_customer_to_dict(
    sync_customer_tenant_customer: SyncCustomerTenantCustomerCommand,
):
    command_dict = sync_customer_tenant_customer.to_dict

    expect(command_dict).to(be_a(dict))
    expect(command_dict).to(
        have_keys(
            {
                'tenant_id': str(sync_customer_tenant_customer.tenant_id),
                'tenant_customer_id': str(sync_customer_tenant_customer.tenant_customer_id),
                'payment_provider': str(sync_customer_tenant_customer.payment_provider),
            }
        )
    )


def test_sync_customer_tenant_customer_from_dict(
    sync_customer_tenant_customer: SyncCustomerTenantCustomerCommand,
):
    command_instance = SyncCustomerTenantCustomerCommand.from_dict(
        sync_customer_tenant_customer.to_dict
    )

    expect(command_instance).to(be_a(SyncCustomerTenantCustomerCommand))
    expect(command_instance).to(equal(sync_customer_tenant_customer))

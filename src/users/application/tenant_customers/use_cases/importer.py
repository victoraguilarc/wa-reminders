import logging
import uuid
from dataclasses import dataclass
from typing import List, Optional

from src.common.application.commands.memberships import RegisterMembershipPurchaseCommand
from src.common.application.queries.memberships import (
    GetActiveMembershipQuery,
    GetMembershipPlanByAliasQuery,
)
from src.common.application.queries.payments import GetManualPaymentMethodQuery
from src.common.constants import DEFAULT_LANGUAGE
from src.common.domain.data.countries import CountryConfigBuilder
from src.common.domain.enums.payments import PaymentProvider, PaymentProviderStrategy
from src.common.domain.enums.users import TenantCustomerCreationSource
from src.common.domain.exceptions.memberships import MembershipPlanNotFound
from src.common.domain.exceptions.payments import PaymentMethodNotFound
from src.common.domain.messaging.commands import CommandBus
from src.common.domain.messaging.queries import QueryBus
from src.common.domain.models.country_config import CountryConfig
from src.common.domain.models.email_address import EmailAddress
from src.common.domain.models.membership_plan import MembershipPlan
from src.common.domain.models.membership_purchase_item import MembershipPurchaseItem
from src.common.domain.models.payment_method import PaymentMethod
from src.common.domain.models.phone_number import PhoneNumber
from src.common.domain.models.tenant import Tenant
from src.common.domain.models.tenant_customer import TenantCustomer
from src.common.domain.models.user import User
from src.common.domain.value_objects import (
    EmailAddressId,
    MembershipPurchaseItemId,
    PhoneNumberId,
    RawPhoneNumber,
    TenantCustomerId,
    UserId,
)
from src.memberships.domain.entities.membership_purchase_params import MembershipPurchaseParams
from src.users.domain.repositories import TenantCustomerRepository
from src.users.domain.repositories.email_address import EmailAddressRepository
from src.users.domain.repositories.phone_number import PhoneNumberRepository
from src.users.domain.types.import_item import TenantCustomerImportItem


@dataclass
class TenantCustomersImporter(object):
    tenant: Tenant
    import_items: List[TenantCustomerImportItem]
    email_repository: EmailAddressRepository
    phone_repository: PhoneNumberRepository
    tenant_customer_repository: TenantCustomerRepository
    query_bus: QueryBus
    command_bus: CommandBus
    country_config: CountryConfig
    run_async_commands: bool = False

    def execute(self):
        for import_item in self.import_items:
            if not import_item.email and not import_item.phone_number:
                logging.info(
                    f'Importer: skipped alias={import_item.alias} no email nor phone_number'
                )
                continue

            tenant_customer: TenantCustomer = self._import_tenant_customer(import_item)
            if not import_item.plan_alias:
                logging.info(f'Importer: skipped alias={import_item.alias} no membership_plan')
                continue

            membership_plan: MembershipPlan = self._get_membership_plan(import_item)
            payment_method: PaymentMethod = self._get_manual_payment_method()
            self._import_membership(
                tenant_customer=tenant_customer,
                membership_plan=membership_plan,
                import_item=import_item,
                payment_method=payment_method,
            )

    def _import_tenant_customer(
        self,
        import_item: TenantCustomerImportItem,
    ) -> TenantCustomer:
        tenant_customer = self._get_existent_tenant_customer(import_item)

        if tenant_customer:
            return tenant_customer

        return self.tenant_customer_repository.persist(
            instance=TenantCustomer(
                id=TenantCustomerId(uuid.uuid4()),
                tenant_id=self.tenant.id,
                email_address=self._email_address(import_item),
                phone_number=self._get_phone_number(import_item),
                user=User(
                    id=UserId(uuid.uuid4()),
                    current_tenant_id=None,
                    is_active=True,
                    email_address=None,
                    phone_number=None,
                    created_at=import_item.created_at,
                ),
                first_name=import_item.first_name,
                paternal_surname=import_item.paternal_surname,
                maternal_surname=import_item.maternal_surname,
                birth_date=None,
                gender=None,
                creation_source=TenantCustomerCreationSource.UNDEFINED,
                lang=DEFAULT_LANGUAGE,
                status=import_item.status,
                created_at=import_item.created_at,
                photo=None,
                photo_url=None,
            ),
        )

    def _get_existent_tenant_customer(
        self,
        import_item: TenantCustomerImportItem,
    ) -> Optional[TenantCustomer]:
        country_config = CountryConfigBuilder.from_iso_code(self.tenant.country_iso_code)
        if import_item.email:
            return self.tenant_customer_repository.find_by_email(
                tenant_id=self.tenant.id,
                email=import_item.email,
            )
        if import_item.phone_number:
            return self.tenant_customer_repository.find_by_phone_number(
                tenant_id=self.tenant.id,
                phone_number=RawPhoneNumber(
                    iso_code=country_config.iso_code,
                    dial_code=import_item.dial_code or country_config.dial_code,
                    phone_number=import_item.phone_number,
                    prefix=None,
                ),
            )
        if import_item.alias:
            return self.tenant_customer_repository.find_by_alias(
                tenant_id=self.tenant.id,
                alias=import_item.alias,
            )
        return None

    def _get_membership_plan(self, import_item) -> MembershipPlan:
        membership_plan: Optional[MembershipPlan] = self.query_bus.ask(
            query=GetMembershipPlanByAliasQuery(
                tenant_id=self.tenant.id,
                alias=import_item.plan_alias,
            )
        )
        if not membership_plan:
            raise MembershipPlanNotFound
        return membership_plan

    def _import_membership(
        self,
        tenant_customer: TenantCustomer,
        membership_plan: MembershipPlan,
        import_item: TenantCustomerImportItem,
        payment_method: PaymentMethod,
    ):
        membership = self.query_bus.ask(
            query=GetActiveMembershipQuery(
                tenant_id=self.tenant.id,
                tenant_customer_id=tenant_customer.id,
                membership_plan_id=membership_plan.id,
            )
        )

        if membership:
            logging.info(f'Importer: skipped alias={import_item.alias} membership already imported')
            return

        self.command_bus.dispatch(
            command=RegisterMembershipPurchaseCommand(
                tenant=self.tenant,
                creation_params=MembershipPurchaseParams(
                    tenant=self.tenant,
                    membership_plan=membership_plan,
                    items=[
                        MembershipPurchaseItem(
                            id=MembershipPurchaseItemId(uuid.uuid4()),
                            tenant_customer=tenant_customer,
                        ),
                    ],
                    amount=import_item.initial_amount,
                    payment_method=payment_method,
                ),
                initial_amount=import_item.initial_amount,
                redemption_authorized=True,
                send_async_emails=self.run_async_commands,
            ),
        )

    def _get_manual_payment_method(self) -> Optional[PaymentMethod]:
        payment_method: Optional[PaymentMethod] = self.query_bus.ask(
            query=GetManualPaymentMethodQuery(
                tenant_id=self.tenant.id,
                provider=PaymentProvider.MANUAL,
                provider_strategy=PaymentProviderStrategy.CASH,
            ),
        )
        if not payment_method:
            raise PaymentMethodNotFound
        return payment_method

    def _email_address(
        self,
        import_item: TenantCustomerImportItem,
    ) -> Optional[EmailAddress]:
        if not import_item.email:
            return None

        email_address = self.email_repository.find(email=import_item.email)
        if email_address:
            return email_address

        return self.email_repository.persist(
            instance=EmailAddress(
                id=EmailAddressId(uuid.uuid4()),
                email=import_item.email,
            ),
        )

    def _get_phone_number(
        self,
        import_item: TenantCustomerImportItem,
    ) -> Optional[PhoneNumber]:
        if not import_item.phone_number:
            return None

        dial_code = import_item.dial_code or self.country_config.dial_code
        phone_number = self.phone_repository.find(
            dial_code=dial_code, phone_number=import_item.phone_number
        )
        if phone_number:
            return phone_number

        return self.phone_repository.persist(
            instance=PhoneNumber(
                id=PhoneNumberId(uuid.uuid4()),
                iso_code=self.country_config.iso_code,
                dial_code=dial_code,
                phone_number=import_item.phone_number,
                is_verified=False,
                prefix=None,
            ),
        )

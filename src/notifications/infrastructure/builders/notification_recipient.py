from src.common.database.models import TenantCustomerORM
from src.common.domain.enums.countries import CountryIsoCode
from src.common.domain.value_objects import RawPhoneNumber, TenantCustomerId
from src.notifications.domain.notification_recipient import NotificationRecipient


class NotificationRecipientBuilder(object):
    @classmethod
    def from_tenant_customer(cls, orm_instance: TenantCustomerORM) -> NotificationRecipient:
        return NotificationRecipient(
            id=TenantCustomerId(orm_instance.uuid),
            first_name=orm_instance.first_name,
            paternal_surname=orm_instance.paternal_surname,
            maternal_surname=orm_instance.maternal_surname,
            phone_number=(
                RawPhoneNumber(
                    iso_code=CountryIsoCode.from_value(
                        orm_instance.phone_number.iso_code,
                    ),
                    dial_code=orm_instance.phone_number.dial_code,
                    phone_number=orm_instance.phone_number.phone_number,
                    prefix=orm_instance.phone_number.prefix,
                )
                if orm_instance.phone_number and orm_instance.phone_number.is_verified
                else None
            ),
            email=Email(orm_instance.user.email),
        )

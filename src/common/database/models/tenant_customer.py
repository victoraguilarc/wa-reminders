# -*- coding: utf-8 -*-

from typing import Optional

from django.db import models

from src.common.database.models.mixins.tenants import UUIDTimestampTenantMixin
from src.common.database.models.mixins.users import AuthMixin, ProfileMixin
from src.common.domain.enums.users import TenantCustomerStatus, TenantCustomerCreationSource


class TenantCustomerORM(UUIDTimestampTenantMixin, AuthMixin, ProfileMixin):
    user = models.ForeignKey(
        'UserORM',
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='customers',
    )
    status = models.CharField(
        verbose_name='Status',
        choices=TenantCustomerStatus.choices(),
        max_length=25,
        default=str(TenantCustomerStatus.NEW),
    )
    creation_source = models.CharField(
        verbose_name='Creation Source',
        choices=TenantCustomerCreationSource.choices(),
        max_length=50,
        default=str(TenantCustomerCreationSource.UNDEFINED),
    )

    @property
    def phone(self) -> Optional[str]:
        return self.phone_number.display_phone_number if self.phone_number else None

    @property
    def email(self) -> Optional[str]:
        return self.email_address.email if self.email_address else None

    @property
    def is_active(self) -> bool:
        return self.status == TenantCustomerStatus.ACTIVE

    def save(self, **kwargs):
        super().save(**kwargs)

    def __str__(self):
        if self.email_address:
            return f'{self.email_address.email}/{self.tenant}'
        if self.phone_number:
            return f'{self.phone_number.phone_number}/{self.tenant}'
        return str(self.uuid)

    class Meta:
        db_table = 'tenant_customers'
        verbose_name = 'Tenant Customer'
        verbose_name_plural = 'Tenant Customers'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'tenant'),
                name='unique_tenant_customer',
            ),
            models.UniqueConstraint(
                fields=('tenant', 'email_address'),
                name='unique_tenant_customer_email_address',
            ),
            models.UniqueConstraint(
                fields=('tenant', 'phone_number'),
                name='unique_tenant_customer_phone_number',
            ),
        )

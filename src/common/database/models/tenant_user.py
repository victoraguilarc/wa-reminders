# -*- coding: utf-8 -*-

from typing import Optional

from django.db import models

from src.common.database.models.mixins.tenants import UUIDTimestampTenantMixin
from src.common.database.models.mixins.users import ProfileMixin
from src.common.domain.enums.users import TenantCustomerStatus, TenantUserStatus


class TenantUserORM(UUIDTimestampTenantMixin, ProfileMixin):
    user = models.ForeignKey(
        'UserORM',
        verbose_name='User',
        on_delete=models.CASCADE,
    )
    is_owner = models.BooleanField(
        verbose_name='Is Owner',
        default=False,
    )
    status = models.CharField(
        verbose_name='Status',
        choices=TenantUserStatus.choices(),
        max_length=25,
        default=str(TenantUserStatus.PENDING),
    )

    @property
    def display_email(self) -> Optional[str]:
        return self.user.email_address.email if self.user.email_address else '---'

    @property
    def display_phone_number(self) -> Optional[str]:
        return self.user.phone_number.display_phone_number if self.user.phone_number else '---'

    @property
    def is_active(self) -> bool:
        return self.status == TenantCustomerStatus.ACTIVE

    @property
    def is_inactive(self) -> bool:
        return self.status == TenantCustomerStatus.INACTIVE

    def save(self, **kwargs):
        super().save(**kwargs)

    def __str__(self):
        if self.user.email_address:
            return f'{self.user.email_address.email}/{self.tenant}'
        if self.user.phone_number:
            return f'{self.user.phone_number.display_phone_number}/{self.tenant}'
        return str(self.uuid)

    class Meta:
        db_table = 'tenant_users'
        verbose_name = 'Tenant User'
        verbose_name_plural = 'Tenant Users'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'tenant'),
                name='unique_tenant_user',
            ),
        )

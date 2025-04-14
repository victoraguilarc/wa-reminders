# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from src.common.database.models import TenantCustomerORM
from src.common.database.resources.tenant_customer import TenantCustomerAdminResource
from src.common.presentation.utils.admin_widgets import RelatedDropdownFilter


@admin.register(TenantCustomerORM)
class TenantCustomerAdmin(ImportExportModelAdmin):
    resource_classes = (TenantCustomerAdminResource,)
    search_fields = (
        'email_address__email',
        'phone_number__phone_number',
        'uuid',
        'first_name',
        'paternal_surname',
        'maternal_surname',
    )
    list_display = (
        'uuid',
        'view_email',
        'view_phone_number',
        'view_tenant',
        'view_name',
        'status',
        'created_at',
    )
    raw_id_fields = (
        'user',
        'tenant',
        'email_address',
        'phone_number',
    )
    list_filter = (
        'status',
        ('tenant', RelatedDropdownFilter),
    )

    def view_tenant(self, instance: TenantCustomerORM):
        return instance.tenant.name

    def view_email(self, instance: TenantCustomerORM):
        if not instance.email_address:
            return '---'
        verification_icon = '✔' if instance.email_address.is_verified else ''
        return f'{verification_icon}{instance.email_address.email} '

    def view_phone_number(self, instance: TenantCustomerORM):
        if not instance.phone_number:
            return '---'
        verification_icon = '✔' if instance.phone_number_verified else ''
        return f'{verification_icon}{instance.display_phone_number}'

    def view_name(self, instance: TenantCustomerORM):
        return instance.display_name

    view_tenant.short_description = 'Tenant'
    view_email.short_description = 'Email'
    view_phone_number.short_description = 'Phone Number'
    view_name.short_description = 'Full Name'

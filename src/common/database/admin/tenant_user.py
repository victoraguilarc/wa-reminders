# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from src.common.database.models import TenantCustomerORM, TenantUserORM
from src.common.presentation.utils.admin_widgets import RelatedDropdownFilter


@admin.register(TenantUserORM)
class TenantUserAdmin(ImportExportModelAdmin):
    search_fields = (
        'uuid',
        'first_name',
        'paternal_surname',
        'maternal_surname',
        'user__email_address__email',
        'user__phone_number__phone_number',
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
    )
    list_filter = (
        'status',
        ('tenant', RelatedDropdownFilter),
    )

    def view_tenant(self, instance: TenantCustomerORM):
        return instance.tenant.name

    def view_email(self, instance: TenantCustomerORM):
        if not instance.user.email_address:
            return '---'
        verification_icon = '✔' if instance.user.email_address.is_verified else ''
        return f'{verification_icon}{instance.user.email_address.email} '

    def view_phone_number(self, instance: TenantCustomerORM):
        if not instance.user.phone_number:
            return '---'
        verification_icon = '✔' if instance.user.phone_number_verified else ''
        return f'{verification_icon}{instance.user.display_phone_number}'

    def view_name(self, instance: TenantCustomerORM):
        return instance.display_name

    view_tenant.short_description = 'Tenant'
    view_email.short_description = 'Email'
    view_phone_number.short_description = 'Phone Number'
    view_name.short_description = 'Full Name'

from django.contrib import admin


def apply_soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=True)


def revert_soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=False)


class SoftDeleteAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        readonly_fields += ('is_deleted', 'available')
        return readonly_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display += ('available',)
        return list_display

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions[apply_soft_delete.__name__] = (
            apply_soft_delete,
            apply_soft_delete.__name__,
            'Apply Soft Delete',
        )
        actions[revert_soft_delete.__name__] = (
            revert_soft_delete,
            revert_soft_delete.__name__,
            'Revert Soft Delete',
        )
        return actions

    def available(self, obj):
        return obj.is_available

    available.boolean = True
    available.short_description = "Available"

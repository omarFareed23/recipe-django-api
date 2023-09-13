"""
Django adming Customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define user admin pages"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': ('name',)
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        )
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                # password1 and password2 have a predefined logic saved in django
                'fields': ('email', 'password1',  'password2', 'name', 'is_active')
            }
        ),
    )


admin.site.register(models.User, UserAdmin)

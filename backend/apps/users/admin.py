from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, MagicLinkToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'display_name', 'language_preference', 'is_active', 'created_at']
    list_filter = ['is_active', 'language_preference', 'created_at']
    search_fields = ['email', 'display_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Profile', {'fields': ('display_name', 'language_preference', 'timezone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_active_at',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name'),
        }),
    )


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at', 'used_at']
    list_filter = ['created_at', 'used_at']
    search_fields = ['user__email']
    readonly_fields = ['token_hash', 'created_at']

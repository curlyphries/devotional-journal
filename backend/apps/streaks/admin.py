from django.contrib import admin

from .models import UserStreak


@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'total_entries', 'last_entry_date']
    search_fields = ['user__email']
    readonly_fields = ['total_entries']

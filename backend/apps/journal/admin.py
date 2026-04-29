from django.contrib import admin

from .models import JournalEntry


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood_tag', 'created_at']
    list_filter = ['mood_tag', 'date', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['encrypted_content']

from django.contrib import admin

from .models import BibleTranslation, BibleVerse


@admin.register(BibleTranslation)
class BibleTranslationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'language', 'is_public_domain']
    list_filter = ['language', 'is_public_domain']


@admin.register(BibleVerse)
class BibleVerseAdmin(admin.ModelAdmin):
    list_display = ['reference', 'translation']
    list_filter = ['translation', 'book']
    search_fields = ['text', 'book_name']

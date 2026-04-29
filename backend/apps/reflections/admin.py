from django.contrib import admin

from .models import (
    AlignmentTrend,
    DailyReflection,
    LifeArea,
    OpenThread,
    ThreadPrompt,
    UserJourney,
)


@admin.register(LifeArea)
class LifeAreaAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "display_order", "is_active"]
    list_editable = ["display_order", "is_active"]
    ordering = ["display_order"]


@admin.register(UserJourney)
class UserJourneyAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "title",
        "duration_days",
        "current_day",
        "status",
        "started_at",
    ]
    list_filter = ["status", "duration_days", "reading_mode"]
    search_fields = ["user__email", "title"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(DailyReflection)
class DailyReflectionAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "scripture_reference", "journey", "created_at"]
    list_filter = ["date", "journey"]
    search_fields = ["user__email", "scripture_reference"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(AlignmentTrend)
class AlignmentTrendAdmin(admin.ModelAdmin):
    list_display = ["user", "period_type", "period_start", "period_end", "created_at"]
    list_filter = ["period_type"]
    search_fields = ["user__email"]
    readonly_fields = ["id", "created_at"]


@admin.register(OpenThread)
class OpenThreadAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "thread_type",
        "status",
        "days_since_mentioned",
        "followup_count",
        "created_at",
    ]
    list_filter = ["status", "thread_type", "related_life_area"]
    search_fields = ["user__email"]
    readonly_fields = ["id", "created_at", "days_since_mentioned"]


@admin.register(ThreadPrompt)
class ThreadPromptAdmin(admin.ModelAdmin):
    list_display = ["thread", "response", "expanded", "shown_at", "responded_at"]
    list_filter = ["response", "expanded"]
    readonly_fields = ["id", "shown_at"]

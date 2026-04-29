from django.contrib import admin

from .models import ReadingPlan, ReadingPlanDay, UserPlanEnrollment


class ReadingPlanDayInline(admin.TabularInline):
    model = ReadingPlanDay
    extra = 1


@admin.register(ReadingPlan)
class ReadingPlanAdmin(admin.ModelAdmin):
    list_display = ["title_en", "category", "duration_days", "is_premium", "is_active"]
    list_filter = ["category", "is_premium", "is_active"]
    search_fields = ["title_en", "title_es"]
    inlines = [ReadingPlanDayInline]


@admin.register(UserPlanEnrollment)
class UserPlanEnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "current_day", "is_active", "started_at"]
    list_filter = ["is_active", "plan"]
    search_fields = ["user__email"]

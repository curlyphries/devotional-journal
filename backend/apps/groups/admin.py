from django.contrib import admin

from .models import Group, GroupEngagementSnapshot, GroupMembership


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by", "tier", "member_count", "created_at"]
    list_filter = ["tier", "created_at"]
    search_fields = ["name", "created_by__email"]
    inlines = [GroupMembershipInline]
    readonly_fields = ["invite_code"]


@admin.register(GroupEngagementSnapshot)
class GroupEngagementSnapshotAdmin(admin.ModelAdmin):
    list_display = [
        "group",
        "date",
        "total_members",
        "members_active_today",
        "avg_streak",
    ]
    list_filter = ["date", "group"]

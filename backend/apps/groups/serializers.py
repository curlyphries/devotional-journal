"""
Serializers for groups.
"""

from rest_framework import serializers

from .models import Group, GroupEngagementSnapshot, GroupMembership


class GroupMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_display_name = serializers.CharField(
        source="user.display_name", read_only=True
    )

    class Meta:
        model = GroupMembership
        fields = [
            "id",
            "user_email",
            "user_display_name",
            "role",
            "joined_at",
            "is_active",
        ]


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(
        source="created_by.display_name", read_only=True
    )

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "created_by_name",
            "invite_code",
            "active_plan",
            "max_members",
            "tier",
            "member_count",
            "created_at",
        ]
        read_only_fields = ["id", "invite_code", "created_at"]


class GroupDetailSerializer(GroupSerializer):
    memberships = GroupMembershipSerializer(many=True, read_only=True)

    class Meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields + ["memberships"]


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "description", "max_members"]


class GroupEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEngagementSnapshot
        fields = [
            "date",
            "total_members",
            "members_active_today",
            "avg_streak",
            "plan_completion_pct",
        ]


class JoinGroupSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=8)

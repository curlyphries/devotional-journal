"""
Views for group management (Phase 2).
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, GroupEngagementSnapshot, GroupMembership
from .serializers import (
    GroupCreateSerializer,
    GroupDetailSerializer,
    GroupEngagementSerializer,
    GroupSerializer,
    JoinGroupSerializer,
)


class GroupListCreateView(APIView):
    """
    List user's groups or create a new group.
    """

    def get(self, request):
        memberships = GroupMembership.objects.filter(
            user=request.user, is_active=True
        ).select_related("group")

        groups = [m.group for m in memberships]
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = Group.objects.create(
            created_by=request.user, **serializer.validated_data
        )

        GroupMembership.objects.create(group=group, user=request.user, role="leader")

        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupDetailView(APIView):
    """
    Get group details.
    """

    def get_group(self, group_id, user):
        try:
            membership = GroupMembership.objects.select_related("group").get(
                group_id=group_id, user=user, is_active=True
            )
            return membership.group, membership
        except GroupMembership.DoesNotExist:
            return None, None

    def get(self, request, group_id):
        group, membership = self.get_group(group_id, request.user)
        if not group:
            return Response(
                {"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = GroupDetailSerializer(group)
        return Response(serializer.data)


class JoinGroupView(APIView):
    """
    Join a group via invite code.
    """

    def post(self, request, group_id):
        serializer = JoinGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if group.invite_code != serializer.validated_data["invite_code"]:
            return Response(
                {"error": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST
            )

        if group.member_count >= group.max_members:
            return Response(
                {"error": "Group is full"}, status=status.HTTP_400_BAD_REQUEST
            )

        membership, created = GroupMembership.objects.get_or_create(
            group=group, user=request.user, defaults={"role": "member"}
        )

        if not created and not membership.is_active:
            membership.is_active = True
            membership.save()

        return Response(GroupSerializer(group).data)


class LeaveGroupView(APIView):
    """
    Leave a group.
    """

    def delete(self, request, group_id):
        try:
            membership = GroupMembership.objects.get(
                group_id=group_id, user=request.user, is_active=True
            )
        except GroupMembership.DoesNotExist:
            return Response({"error": "Not a member"}, status=status.HTTP_404_NOT_FOUND)

        if (
            membership.role == "leader"
            and membership.group.memberships.filter(
                role="leader", is_active=True
            ).count()
            == 1
        ):
            return Response(
                {
                    "error": "Cannot leave - you are the only leader. Transfer leadership first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.is_active = False
        membership.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupEngagementView(APIView):
    """
    Get aggregate engagement metrics (leaders only).
    """

    def get(self, request, group_id):
        try:
            membership = GroupMembership.objects.get(
                group_id=group_id, user=request.user, is_active=True
            )
        except GroupMembership.DoesNotExist:
            return Response({"error": "Not a member"}, status=status.HTTP_404_NOT_FOUND)

        if not membership.is_leader:
            return Response({"error": "Leaders only"}, status=status.HTTP_403_FORBIDDEN)

        snapshots = GroupEngagementSnapshot.objects.filter(group_id=group_id).order_by(
            "-date"
        )[:30]

        serializer = GroupEngagementSerializer(snapshots, many=True)
        return Response(serializer.data)


class SetGroupPlanView(APIView):
    """
    Assign a reading plan to the group (leaders only).
    """

    def post(self, request, group_id):
        try:
            membership = GroupMembership.objects.select_related("group").get(
                group_id=group_id, user=request.user, is_active=True
            )
        except GroupMembership.DoesNotExist:
            return Response({"error": "Not a member"}, status=status.HTTP_404_NOT_FOUND)

        if not membership.is_leader:
            return Response({"error": "Leaders only"}, status=status.HTTP_403_FORBIDDEN)

        plan_id = request.data.get("plan_id")
        if not plan_id:
            return Response(
                {"error": "plan_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

        from apps.plans.models import ReadingPlan

        try:
            plan = ReadingPlan.objects.get(id=plan_id, is_active=True)
        except ReadingPlan.DoesNotExist:
            return Response(
                {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        group = membership.group
        group.active_plan = plan
        group.save()

        return Response(GroupSerializer(group).data)

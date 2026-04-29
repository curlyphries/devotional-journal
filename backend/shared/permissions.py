"""
Custom permission classes for the API.
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsGroupLeader(permissions.BasePermission):
    """
    Permission to check if user is a leader of the group.
    """
    def has_object_permission(self, request, view, obj):
        from apps.groups.models import GroupMembership
        return GroupMembership.objects.filter(
            group=obj,
            user=request.user,
            role__in=['leader', 'admin'],
            is_active=True
        ).exists()

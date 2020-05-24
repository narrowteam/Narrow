from rest_framework import permissions
from tasks.models import Task, SubTaskAssignment
from projects.models import Project


class IsAssigned(permissions.BasePermission):

    # def __init__(self, allowed_methods):
    #     self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return SubTaskAssignment.objects.filter(
            user=request.user,
            sub_task=obj
        ).exist()


class IsProjectOwnerOrParticipant(permissions.BasePermission):

    # def __init__(self, allowed_methods):
    #     self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.participants.all()


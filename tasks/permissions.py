from rest_framework import permissions
from tasks.models import TaskPermission, Task
from projects.models import Project


class IsPermittedToEdit(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return TaskPermission.objects.filter(
            owner=request.user,
            target=obj,
            permission_type='EDIT'
        ).exists()

    def has_permission(self, request, view):
        return True


class IsPermittedToView(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return TaskPermission.objects.filter(
            owner=request.user,
            target=obj,
            permission_type='READ'
        ).exists()

    def has_permission(self, request, view):
        return True


class IsPermittedToManagePermissions:

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        task = Task.objects.get(pk=obj.target.pk)
        project = Project.objects.get(id=task.project.id)

        # Only project owner is permitted
        return request.user == project.owner



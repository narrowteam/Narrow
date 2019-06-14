from rest_framework import permissions
from tasks.models import TaskPermission, Task
from projects.models import Project


class IsPermittedToEdit(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return self.look_up_for_permission_in_task_tree(request.user, obj)

    def look_up_for_permission_in_task_tree(self, user, obj):
        permission = TaskPermission.objects.filter(
            owner=user,
            target=obj,
            permission_type='EDIT'
        )
        if permission.exists():
            return True
        else:
           return self.check_parent(user, obj)

    def check_parent(self, user, obj):
        if obj.is_main:
            return False
        else:
            parent_obj = Task.objects.get(id=obj.parent_id)
            return self.look_up_in_task_tree(user, parent_obj)


    def has_permission(self, request, view):
        return True


class IsPermittedToView(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return self.look_up_for_permission_in_task_tree(request.user, obj)

    def look_up_for_permission_in_task_tree(self, user, obj):
        permission = TaskPermission.objects.filter(
            owner=user,
            target=obj,
            permission_type='READ'
        )
        if permission.exists():
            return True
        else:
            return self.check_parent(user, obj)

    def check_parent(self, user, obj):
        if obj.is_main:
            return False
        else:
            parent_obj = Task.objects.get(id=obj.parent_id)
            return self.look_up_in_task_tree(user, parent_obj)

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



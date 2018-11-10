from rest_framework import permissions


class IsSelf(permissions.BasePermission):

    # def __init__(self, allowed_methods):
    #     self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

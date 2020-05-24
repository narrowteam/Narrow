from rest_framework import permissions


class IsOwnerOrParticipant(permissions.BasePermission):

    # def __init__(self, allowed_methods):
    #     self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.participants.all()


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsInviting(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
        # return request.method in self.allowed_methods

    def has_object_permission(self, request, view, obj):
        return request.user == obj.project.owner

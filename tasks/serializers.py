from rest_framework import serializers

from UserManagement.serializers import UserSerializer
from UserManagement.models import User
from django.db.models import Q, Subquery

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'parent_task',
            'name',
            'description',
            'created_at',
            'updated_at',
            'sub_tasks'
        )
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'sub_tasks': {
                'read_only': True
            },
            'description': {
                'required': False
            },
            'project': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            }
        }

    def get_sub_tasks(self, obj):
        sub_tasks = obj.get_sub_tasks()
        return TaskSerializer(sub_tasks, many=True).data

class TaskPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'owner',
            'target',
            'permission_type',
        )







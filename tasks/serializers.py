from rest_framework import serializers

from UserManagement.serializers import UserSerializer
from UserManagement.models import User
from django.db.models import Q, Subquery

from tasks.models import Task, TaskPermission


class TaskSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'project',
            'name',
            'description',
            'created_at',
            'updated_at',
            'sub_tasks',
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

    def create(self, validated_data):
        try:
            task_creator = self.context.get('request').user
        except AttributeError:
            print("Provide request in context")
            raise
        task = Task.objects.create(**validated_data)
        TaskPermission.objects.create(
            owner=task_creator,
            target=task,
            permission_type="EDIT",
        )
        return task

    def get_sub_tasks(self, obj):
        sub_tasks = obj.get_sub_tasks()
        return TaskSerializer(sub_tasks, many=True).data


class TaskPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model =TaskPermission
        fields = (
            'owner',
            'target',
            'permission_type',
        )







from rest_framework import serializers

from UserManagement.serializers import UserSerializer
from UserManagement.models import User
from django.db.models import Q, Subquery

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'pk',
            'project',
            'parent_task',
            'name',
            'description',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'pk': {
                'required': True
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






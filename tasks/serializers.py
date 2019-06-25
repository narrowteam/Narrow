from rest_framework import serializers
from UserManagement.serializers import BasicUserDataSerializer
from UserManagement.models import User


from tasks.models import Task, Task, SubTask, SubTaskAssignment
from cdn.models import TaskFile


class SubTaskSerializer(serializers.Serializer):
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = SubTask
        fields = (
            'name',
            'description',
            'assigned_users'
        )

    def get_assigned_users(self, obj):
        return BasicUserDataSerializer(
            User.objects.filter(
                subTaskAssignments__in=SubTaskAssignment.objects.filter(
                    sub_task=obj,
                )
            )
        )


class TaskSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField()
    name = serializers.CharField(min_length=4)

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
        return task

    def get_sub_tasks(self, obj):
        sub_tasks = obj.get_sub_tasks()
        return SubTaskSerializer(sub_tasks, many=True).data


class SubTaskAssignmentSerializer(serializers.Serializer):
    users = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    task = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        assignments = self._make_assignments_list(
            users=validated_data['users'],
            task=validated_data['task']
        )
        SubTaskAssignment.objects.bulk_create(assignments)
        return assignments

    def _make_assignments_list(self, users, task):
        return [
            SubTaskAssignment(
                    user=u,
                    task=task
                )
            for u in users
        ]


class SubTaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile()
        fields = (
            'file',
            'sub_task',
            'owner'
        )
        extra_kwargs = {
            'sub_tasks': {
                'required': False,
                'read_only': True
            },
            'owner': {
                'required': False,
                'read_only': True
            }
        }









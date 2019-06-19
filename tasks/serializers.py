from rest_framework import serializers
from UserManagement.serializers import UserSerializer
from UserManagement.models import User


from tasks.models import Task, Task, SubTask, SubTaskAssignment


class SubTaskSerializer(serializers.Serializer):

    class Meta:
        model = SubTask
        fields = (
            'name',
            'description',
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
        return TaskSerializer(sub_tasks, many=True).data


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







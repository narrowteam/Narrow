from rest_framework import serializers

from .models import Project, ProjectInvitation
from UserManagement.serializers import UserSerializer, BasicUserDataSerializer
from UserManagement.models import User
from django.db.models import Q, Subquery
from utils.parsers import EmailOrIdUserList
from tasks.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    participants__count = serializers.IntegerField(required=False)
    owner = BasicUserDataSerializer(required=False)

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'project_name',
            'description',
            'participants__count',

        )
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'owner': {
                'read_only': True
            },
            'project_name': {
                'required': True
            },
            'description': {
                'required': False
            },
            'participants__count': {
                'read_only': True,
            },
        }

class ProjectDetailSerializer(ProjectSerializer):
    participants = BasicUserDataSerializer(required=False, many=True)
    owner = BasicUserDataSerializer(required=False)
    main_task = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'project_name',
            'description',
            'participants',
            'main_task',
        )
        extra_kwargs = {
            'id': {
                'read_only': True,
                'required': False
            },
            'owner': {
                'read_only': True,
                'required': False
            },
            'project_name': {
                'required': True
            },
            'description': {
                'required': False
            },
            'participants': {
                'required': False,
                'read_only': True
            },
        }

    def get_main_task(self, obj):
        task = obj.assignedTasks.get(is_main=True)
        return TaskSerializer(task).data


class ProjectPatchSerializer(ProjectSerializer):
    class Meta:
        model = Project
        fields = (
            'project_name',
            'description'
        )
        extra_kwargs = {
            'project_name': {
                'required': False
            },
            'description': {
                'required': False
            },
        }

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        return instance


# Nested serializer used to validate lists of emails or ids
class IdOrEmailListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)


'''
    Used for serialize list of objects including id ot email (one of) and create invitations
'''
class UsersToInviteListSerializer(serializers.Serializer):
    invitations_list = IdOrEmailListSerializer(many=True, required=True)
    project = serializers.IntegerField(read_only=True)

    def create(self, validated_data):

        '''
            Validated data is set of dictionaries with optional
            user id or email (one of or both)
        '''

        list = EmailOrIdUserList(validated_data['invitations_list'])
        users = list.get_user_models()

        # Creates list of invitation objects assigned to same project
        invs = self._make_list_of_invitations(users, validated_data['project'])

        # Saves it to database
        invitations =ProjectInvitation.objects.bulk_create(invs)
        return invitations

    def _make_list_of_invitations(self, users, project):
        invs = []
        for user in users:
            invs.append(
                ProjectInvitation(
                    owner=user,
                    project=project,
                ))
        return invs


class UsersToRemoveListSerializer(serializers.Serializer):
    to_remove_list = IdOrEmailListSerializer(many=True)
    project = ProjectSerializer(read_only=True)

    def create(self, validated_data):
        list = EmailOrIdUserList(validated_data['to_remove_list'])
        users_to_remove = list.get_user_models()
        validated_data['project'].remove_participants(users_to_remove)
        return users_to_remove

# Serializer only for read
class InvitationListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False)
    owner = BasicUserDataSerializer(required=False)

    class Meta:
        model = ProjectInvitation()
        fields = (
            'id',
            'owner',
            'project',
            'is_accepted',
        )
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'project': {
                'read_only': True,
                'required': False
            },
            'is_accepted': {
                'read_only': True
            },
            'owner': {
                'read_only': True,
                'required': False
            },
        }
# class InvitationListSerializer(serializers.Serializer):
#     invited_users= InvitationSerializer(many=True)

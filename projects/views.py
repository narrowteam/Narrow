from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from UserManagement.models import User
from rest_framework.decorators import action
from projects.serializers import ProjectSerializer, ProjectDetailSerializer,  ProjectPatchSerializer, \
                                    UsersToInviteListSerializer, InvitationListSerializer, \
                                    UsersToRemoveListSerializer

from .permissions import IsOwnerOrParticipant, IsOwner, IsInviting
from projects.models import Project, Group, ProjectInvitation
from django.db.models import Q, Subquery, Count


class ProjectViewSet(ViewSet):
    queryset = Project.objects.all()

    def create(self, request):
        serializer = ProjectDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_200_OK)

    # Project detail view
    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, project)
        serializer = ProjectDetailSerializer(project, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Returns only projects which user is participant of
    def list(self, request):
        projects = request.user.projectList.all().annotate(Count('participants'))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = ProjectPatchSerializer(data=request.data)
        if serializer.is_valid():
            project = get_object_or_404(self.queryset, pk=pk)
            self.check_object_permissions(request, project)
            serializer.update(project, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=True, methods=['post'], url_path='invite', permission_classes=[IsOwner])
    def invite_user(self, request, pk=None):
        serializer = UsersToInviteListSerializer(data=request.data)

        if serializer.is_valid():
            project = get_object_or_404(self.queryset, pk=pk)
            self.check_object_permissions(request, project)
            serializer.save(project=project)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Gets all invitations related to project TODO return made invitations list
    @action(detail=True, methods=['get'], url_path='get_invitations', url_name='get_invitations', permission_classes = [IsOwner])
    def get_invitations(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(request, project)
        invitations = ProjectInvitation.objects.filter(project=project)

        serializer = InvitationListSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'],url_path='remove_participants', url_name='remove_participants', permission_classes = [IsOwner])
    def remove_participants(self, request, pk=None):
        serializer = UsersToRemoveListSerializer(data=request.data)
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(request, project)

        if serializer.is_valid():
            serializer.save(project=project)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            permission_classes.append(IsOwnerOrParticipant)
        else:
            permission_classes.append(IsOwner)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset


class InvitationViewSet(GenericViewSet):
    queryset = ProjectInvitation.objects.all()

    # Returns all invites for request user
    def list(self, request):
        invitations = request.user.invited_to.all()
        # invitations = ProjectInvitation.objects.filter(owner=request.user)
        serializer = InvitationListSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Deletes invitation - can be done by inviting or invited (it is rejection or cancelling)
    def destroy(self, request, pk=None):
        invitation = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, invitation)
        invitation.delete_with_duplicates()

        return Response(status=status.HTTP_200_OK)

    # Accepts invitation and adds user to project
    @action(detail=True, methods=['get'], permission_classes=[IsOwner])
    def accept(self, request, pk=None):
        invitation = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, invitation)
        invitation.accept()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsOwner])
    def reject(self, request, pk=None):
        invitation = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, invitation)
        invitation.delete_with_duplicates()
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'accept':
            permission_classes = [IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsInviting]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

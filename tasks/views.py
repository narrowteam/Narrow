from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from projects.models import Project
from tasks.serializers import TaskSerializer, SubTaskAssignmentSerializer, SubTaskFileSerializer
from tasks.models import Task, SubTaskAssignment, SubTask
from rest_framework.viewsets import ViewSet
from rest_framework import mixins, viewsets
from tasks.permissions import IsAssigned, IsProjectOwnerOrParticipant
from projects.permissions import IsOwner

class TaskViewSet(ViewSet):

    queryset = Task.objects.all()

    def create(self, request, project_id=None):
        # TODO add project admin assigment option
        project = get_object_or_404(Project.objects.all(), id=project_id, owner=request.user)
        self.check_object_permissions(request, project)
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, project_id=None):
        project = Project.objects.get(id=project_id)
        self.check_object_permissions(request, project)
        serializer = TaskSerializer(Task.objects.filter(project=project), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def destroy(self, request, project_id=None, pk=None):
        task = get_object_or_404(Task.objects.all(), project__id=project_id, id=pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, project_id=None, pk=None):
        project = get_object_or_404(self.queryset, pk=pk, project=project_id)
        self.check_object_permissions(request, project)
        serializer = TaskSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            project = get_object_or_404(self.queryset, pk=pk)
            self.check_object_permissions(request, project)
            serializer.update(project, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=True, methods=['post'], url_path='push_sub_task', permission_classes=[IsAuthenticated])
    def push_sub_task(self, request, pk=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            parent_task = get_object_or_404(self.queryset, pk=pk)
            parent_task.push_sub_task(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [IsProjectOwnerOrParticipant]

        elif self.action == 'list':
            permission_classes = [IsProjectOwnerOrParticipant]
        else:
            permission_classes = [IsOwner]
        permission_classes.append(IsAuthenticated)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset


class SubTaskAssignmentViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = SubTaskAssignment.objects.all()

    def create(self, request, project_id=None, *args, **kwargs):
        project = get_object_or_404(Project.objects.all(), id=project_id)
        serializer = SubTaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destory(self, request, pk=None):
        permission = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, permission)
        permission.delete()
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset


class SubTasksView(viewsets.ViewSet):
    queryset = SubTask.objects.all()

    @action(methods=['get'], detail=True)
    def complete(self, request, pk=None):
        sub_task = get_object_or_404(self.queryset, id=pk)
        self.check_object_permissions(request, sub_task)
        sub_task.complete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def upload_file(self, request, pk=None):
        serializer = SubTaskFileSerializer(data=request.data)
        if serializer.is_valid():
            sub_task = get_object_or_404(self.queryset, id=pk)
            self.check_object_permissions(request, sub_task)
            serializer.save(sub_task=sub_task, owner=request.user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_queryset(self):
        return self.queryset

    def get_permissions(self):
        permission_classes = [IsAssigned]
        return [permission() for permission in permission_classes]


# class TaskPermissionViewSet(mixins.CreateModelMixin,
#                             mixins.DestroyModelMixin,
#                             viewsets.GenericViewSet):
#     queryset = TaskPermission.objects.all()
#
#     def create(self, request, project_id=None, *args, **kwargs):
#         project = get_object_or_404(Project.objects.all(), id=project_id)
#         serializer = TaskPermissionSerializer(data=request.data)
#         if serializer.is_valid(): # Needs validation if project exists
#             serializer.save(project=project)
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
#
#     def destory(self, request, pk=None):
#         permission = get_object_or_404(self.queryset, pk=pk)
#         self.check_object_permissions(request, permission)
#         permission.delete()
#         return Response(status=status.HTTP_200_OK)
#
#     def get_permissions(self):
#         permission_classes = [IsPermittedToManagePermissions]
#         return [permission() for permission in permission_classes]
#
#     def get_queryset(self):
#         return self.queryset

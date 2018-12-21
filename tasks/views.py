from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from tasks.serializers import TaskSerializer
from tasks.models import Task

from rest_framework import viewsets, mixins


class TaskViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Task.objects.all()

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
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
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # if self.action == 'retrieve':
        #     permission_classes = [IsOwnerOrParticipant]
        # if self.action == 'create' or self.action == 'destroy' or self.action == 'retrieve' :
        #     permission_classes = [IsAuthenticated]
        # elif self.action == 'get_project_tasks':
        #     permission_classes = [IsAuthenticated]
        # else:
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset

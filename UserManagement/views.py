from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSelf
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, UserPatchSerializer, UserSetPasswordSerializer
from .models import User
from django.db.models import Q, Subquery
from rest_framework.decorators import action
# from rest_framework.generics import CreateAPIView, UpdateAPIView,


class UserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    # Creates new user
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Allows to update all user attributes
    def customize(self, request):
        user = get_object_or_404(self.queryset, id=request.user.id)
        serializer = UserPatchSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()  # check it to use save
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def self_retrieve(self, request):
        user = get_object_or_404(self.queryset, id=request.user.id)
        serializer = UserPatchSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def set_password(self, request):
        user = get_object_or_404(self.queryset, id=request.user.id)
        serializer = UserSetPasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSelf]
        return [permission() for permission in permission_classes]

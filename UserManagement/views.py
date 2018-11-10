from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSelf
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, UserPatchSerializer
from .models import User
from django.db.models import Q, Subquery


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
    def partial_update(self, request, pk=None):
        user = User.objects.get(id=pk)
        self.check_object_permissions(self.request, user)

        serializer = UserPatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data) #check it to use save
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

    # WONT BE USED THAT WAY
    # def retrieve(self, request, pk=None):
    #   user = get_object_or_404(self.queryset, id=pk)
    #   print("IM HERE")
    #   serializer = UserSerializer(user)
    #   return Response(serializer.data)
    # def list(self, request):
    #   serializer = UserSerializer(self.queryset, many=True)
    #   return Response(serializer.data)

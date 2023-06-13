from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet
from kidmeet_app.serializers import *
from kidmeet_app.serializers.users_parents import ParentsSerializer


class ParentsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH','DELETE']:
            return request.user.is_staff
        return True


class ParentsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = User.objects.all()

    permission_classes = [ParentsPermissions]
    # authentication_classes = [JWTAuthentication]

    # we need different serializers for different actions
    serializer_class = ParentsSerializer







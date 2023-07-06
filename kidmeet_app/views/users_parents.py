from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from kidmeet_app.serializers import *
from kidmeet_app.serializers.auth import UserSerializer
from kidmeet_app.serializers.users_parents import ParentsSerializer


class ParentsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        return view.action == 'retrieve' or obj.created_by == request.user


# class ParentsViewSet(mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.ListModelMixin,
#                      GenericViewSet):
    # we need different serializers for different actions
    # serializer_class = ParentsSerializer
    # queryset = User.objects.all()
    # permission_classes = [ParentsPermissions]
    # authentication_classes = [JWTAuthentication]


@api_view(['GET'])
def get_all_parents(request):
    all_parents = User.objects.all()
    serializer = ParentsSerializer(instance=all_parents, many=True)
    return Response(data=serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_parent(request, parent_id):
    parent = get_object_or_404(User, id=parent_id)
    if request.method in ('PUT', 'PATCH'):
        serializer = UserSerializer(
            instance=parent, data=request.data, partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    else:
        parent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)














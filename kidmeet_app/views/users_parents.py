from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from kidmeet_app.models import UserDetails
from kidmeet_app.serializers import *
from kidmeet_app.serializers.auth import UserSerializer
from kidmeet_app.serializers.users_parents import ParentsSerializer, UserDetailsSerializer


class ParentsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        return view.action == 'retrieve' or obj.created_by == request.user


# @api_view(['GET'])
# def get_all_parents(request):
#     all_parents = User.objects.all()
#     serializer = ParentsSerializer(instance=all_parents, many=True)
#     return Response(data=serializer.data)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def get_parent(request, parent_id):
#     parent = get_object_or_404(User, id=parent_id)
#     if request.method in ('PUT', 'PATCH'):
#         serializer = UserSerializer(
#             instance=parent, data=request.data, partial=request.method == 'PATCH'
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data)
#     else:
#         parent.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_details = serializer.save()
        data = {
            'id': user_details.user.id,
            'email': user_details.user.email,
            'first_name': user_details.user.first_name,
            'last_name': user_details.user.last_name,
            'phone_number': user_details.phone_number,
            'birth_year': user_details.birth_year,
            'address': {
                'city': user_details.address.city,
                'street': user_details.address.street,
                'house_number': user_details.address.house_number
            }
        }

        return JsonResponse(data)















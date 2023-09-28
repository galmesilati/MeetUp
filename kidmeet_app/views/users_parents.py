import os
import uuid

from django.contrib.auth.models import User
from google.cloud import storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from google.oauth2 import service_account
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


@api_view(['POST'])
def upload_profile_img(request):
    bucket_name = 'meet-app'
    file_stream = request.FILES['file'].file
    _, ext = os.path.splitext(request.FILES['file'].name)

    object_name = f"profile_img_{uuid.uuid4()}{ext}"

    credentials = service_account.Credentials.from_service_account_file(
        "/Users/gmsyl/OneDrive/שולחן העבודה/meetup-395918-259ba14a84c8.json")

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_file(file_stream)

    return Response()















from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from kidmeet_app.models import Address
from kidmeet_app.models import UserDetails
from kidmeet_app.serializers.auth import UserSerializer
from kidmeet_app.serializers.users_parents import UserDetailsSerializer, AddressSerializer


@api_view(['POST'])
def signup(request):
    print('signup')
    new_user_serializer = UserDetailsSerializer(data=request.data)
    new_user_serializer.is_valid(raise_exception=True)
    new_user_serializer.save()
    return Response(new_user_serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    user_serializer = UserSerializer(instance=request.user, many=False)
    return Response(data=user_serializer.data)
